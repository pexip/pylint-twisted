"""Brains for helping silence pylint errors/warnings from twisted"""

import astroid

from pylint.checkers import BaseChecker

_DEFER_MODULE = astroid.MANAGER.ast_from_module_name("twisted.internet.defer")
_DEFERRED_IMPL = _DEFER_MODULE["Deferred"]


def _has_decorator(node, decorator):
    """Get whether a node has a decorator"""
    if not node.decorators:
        return False
    return decorator in node.decoratornames()


def _is_inline_callbacks(node):
    """Check whether a FunctionDef node is decorated with defer.inlineCallbacks"""
    return _has_decorator(node, "twisted.internet.defer.inlineCallbacks")


@astroid.inference_tip
def _infer_inline_callbacks(node: astroid.nodes.FunctionDef, context=None):
    """Infer the type of inlineCallbacks."""
    # Mock the function call to return a Deferred
    module = astroid.parse(
        f"""\
from twisted.internet import defer
def {node.name}():
    return defer.Deferred()
"""
    )
    wrapped_func = next(module.igetattr(node.name, context=context))
    # Update the node properties to match the original function
    wrapped_func.lineno = node.lineno
    wrapped_func.col_offset = node.col_offset
    wrapped_func.end_lineno = node.end_lineno
    wrapped_func.end_col_offset = node.end_col_offset
    wrapped_func.parent = node.parent
    # Ensure the args match
    wrapped_func.args = node.args
    # Ensure all decorators get propagated
    wrapped_func.decorators = node.decorators
    return iter([wrapped_func])


astroid.MANAGER.register_transform(
    astroid.FunctionDef, _infer_inline_callbacks, _is_inline_callbacks
)


class DeferInlineCallbacksChecker(BaseChecker):
    """defer.inlineCallbacks checker"""

    name = "defer-inlinecallbacks"
    priority = -1
    msgs = {
        "E6900": (
            "Function decorated with defer.inlineCallbacks does not produce a generator",
            "does-not-produce-generator",
            "A function decorated with defer.inlineCallbacks must produce generator.",
        )
    }

    def _generate_children(self, node):
        try:
            for child in node.get_children():
                # If the function node also contains a function def, ignore these as
                # they will be checked separately
                if isinstance(child, astroid.nodes.FunctionDef):
                    continue
                yield child
                yield from self._generate_children(child)
        except (AttributeError, TypeError):
            yield child

    def _produces_generator(self, node):
        """Determine whether a node produces a generator or not"""
        return any(
            isinstance(n, astroid.nodes.Yield) for n in self._generate_children(node)
        )

    def leave_functiondef(self, node):
        # Ignore any methods that aren't decorated with defer.inlineCallbacks
        if not _is_inline_callbacks(node):
            return

        # Ignore abstract methods as these can have no body, and therefore no yield
        if _has_decorator(node, "abc.abstractmethod"):
            return

        if not self._produces_generator(node):
            self.add_message("does-not-produce-generator", node=node)


class DeferReturnValueChecker(BaseChecker):
    """defer.returnValue checker"""

    name = "defer-returnvalue"
    priority = -1
    msgs = {
        "R6901": (
            "Use of defer.returnValue",
            "legacy-return",
            "A return statement should be used instead of defer.returnValue",
        )
    }

    def visit_call(self, node):
        if not isinstance(node, astroid.Call):
            return
        func = node.func
        if isinstance(func, astroid.Attribute):
            func_name = func.attrname
        elif isinstance(func, astroid.Name):
            func_name = func.name
        else:
            func_name = None

        if func_name == "returnValue":
            self.add_message("legacy-return", node=node)


# == Infer twisted.internet.reactor type ==
# Because of the abhorrent twisted sys.modules hackery, pylint can't find the reactor, so
# we're going to help.
# To find the reactor, we import the default reactor for the platform and mock install it
# to get our hands on the actual reactor that would be used.
# Next we use inspect to get the reactor module/class name.
# Finally, we load this as an AST node and transform the AST to refer to this node whenever
# the reactor module is referenced.


def _get_reactor_impl():
    import inspect
    from unittest import mock
    from twisted.internet.default import install

    with mock.patch("twisted.internet.main.installReactor") as mock_install:
        install()
    reactor = mock_install.call_args[0][0]
    reactor_module_name = inspect.getmodule(reactor).__name__
    reactor_module = astroid.MANAGER.ast_from_module_name(reactor_module_name)
    return reactor_module[type(reactor).__name__].instantiate_class()


_REACTOR_IMPL = _get_reactor_impl()


def _is_reactor_module(module):
    """Check whether a Module node is the twisted reactor"""
    return module.name == "twisted.internet.reactor"


@astroid.inference_tip
def _infer_reactor_module(_module, _context=None):
    return iter([_REACTOR_IMPL])


astroid.MANAGER.register_transform(
    astroid.Module, _infer_reactor_module, _is_reactor_module
)


def register(linter):
    """Required to register the plugin with pylint"""
    linter.register_checker(DeferInlineCallbacksChecker(linter))
    linter.register_checker(DeferReturnValueChecker(linter))
