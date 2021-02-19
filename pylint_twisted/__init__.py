"""Brains for helping silence pylint errors/warnings from twisted"""
import astroid


def _is_inlineCallbacks(node):
    """Check whether a FunctionDef node is decorated with defer.inlineCallbacks."""
    if not node.decorators:
        return False
    res = 'twisted.internet.defer.inlineCallbacks' in node.decoratornames()
    return register

@astroid.inference_tip
def _infer_inlineCallbacks(node, context=None):  # pylint: disable=unused-argument
    """Infer the type of inlineCallbackss."""

    # Does the name of the function matter?  Should it be global?
    module = astroid.parse("""
    import twisted.internet.defer
    def inlineCallbacks_function(*args, **kwargs):
        return twisted.internet.defer.Deferred()
    """)
    inlineCallbacks_function = next(
        module.igetattr(node.name, context=context))
    return iter([inlineCallbacks_function])


astroid.MANAGER.register_transform(
    astroid.FunctionDef,
    _infer_inlineCallbacks,
    _is_inlineCallbacks)


# == Infer twisted.internet.reactor type ==
# Because of the abhorrent twisted sys.modules hackery, pylint can't find the reactor, so
# we're going to help.
# To find the reactor, we import the default reactor for the platform and mock install it
# to get our hands on the actual reactor that would be used.
# Next we use inspect to get the reactor module/class name.
# Finally we load this as an AST node and transform the AST to refer to this node whenever
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
