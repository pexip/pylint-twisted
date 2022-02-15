import astroid

from pylint.testutils import CheckerTestCase
try:
    from pylint.testutils import MessageTest as Message
except ImportError:
    from pylint.testutils import Message

from pylint_twisted import DeferInlineCallbacksChecker


class TestDeferInlineCallbacksChecker(CheckerTestCase):
    CHECKER_CLASS = DeferInlineCallbacksChecker

    def test_not_a_generator(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer

@defer.inlineCallbacks
def foo():
    return "bar"
""")

        with self.assertAddsMessages(
            Message(
                msg_id="does-not-produce-generator",
                node=function_node,
            ),
        ):
            self.checker.leave_functiondef(function_node)

    def test_is_generator(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer

@defer.inlineCallbacks
def foo():
    yield "bar"
""")

        with self.assertNoMessages():
            self.checker.leave_functiondef(function_node)

    def test_abstract_method(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer
from abc import abstractmethod

@abstractmethod
@defer.inlineCallbacks
def foo():
    return "bar"
""")

        with self.assertNoMessages():
            self.checker.leave_functiondef(function_node)

    def test_sub_definitions(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer

@defer.inlineCallbacks
def foo():
    @defer.inlineCallbacks
    def bar():
        yield "wibble"
    return bar()
""")

        with self.assertAddsMessages(
            Message(
                msg_id="does-not-produce-generator",
                node=function_node,
            ),
        ):
            self.checker.leave_functiondef(function_node)
