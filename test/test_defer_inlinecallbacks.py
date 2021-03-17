import pylint_twisted
import pylint.testutils

class DeferInlineCallbacksCheckerTest(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint_twisted.DeferInlineCallbacksChecker

    def test_not_a_generator(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer

@defer.inlineCallbacks
def foo():
    return "bar"
""")

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id="does-not-produce-generator",
                node=function_node,
            ),
        ):
            self.checker.visit_functiondef(function_node)

    def test_is_generator(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer

@defer.inlineCallbacks
def foo():
    yield "bar"
""")

        with self.assertNotMessages():
            self.checker.visit_functiondef(function_node)

    def test_abstract_method(self):
        function_node = astroid.extract_node("""\
from twisted.internet import defer
from abc import abstractmethod

@abstractmethod
@defer.inlineCallbacks
def foo():
    return "bar"
""")

        with self.assertNotMessages():
            self.checker.visit_functiondef(function_node)
