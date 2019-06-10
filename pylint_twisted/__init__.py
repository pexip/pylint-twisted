from __future__ import print_function
"""Brains for helping silence pylint errors/warnings from defer.inlineCallbacks."""
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


def _is_reactor_module(node):
    """Check whether a FunctionDef node is decorated with defer.inlineCallbacks."""
    return node.name == 'twisted.internet.reactor'

@astroid.inference_tip
def _infer_inlineCallbacks(node, context=None):  # pylint: disable=unused-argument
    """Infer the type of inlineCallbackss."""

    # Does the name of the function matter?  Should it be global?
    module = astroid.parse("""
    from twisted.internet import default
    default.install()
    """)
    inlineCallbacks_function = next(
        module.igetattr(node.name, context=context))
    print(inlineCallbacks_function)
    return iter([inlineCallbacks_function])

astroid.MANAGER.register_transform(
    astroid.Module,
    _infer_inlineCallbacks,
    _is_reactor_module)

def register(linter):  # pylint: disable=unused-argument
    """Register the plugin with the linter."""
    pass
