import astroid

from pylint.testutils import CheckerTestCase
try:
    from pylint.testutils import MessageTest as Message
except ImportError:
    from pylint.testutils import Message

from pylint_twisted import DeferReturnValueChecker


class TestDeferReturnValueChecker(CheckerTestCase):
    CHECKER_CLASS = DeferReturnValueChecker

    def test_defer_returnvalue(self):
        call_node = astroid.extract_node("""\
from twisted.internet import defer
defer.returnValue(True)
""")

        with self.assertAddsMessages(
            Message(
                msg_id="legacy-return",
                node=call_node,
            ),
        ):
            self.checker.visit_call(call_node)

    def test_returnvalue(self):
        call_node = astroid.extract_node("""\
from twisted.internet.defer import returnValue
returnValue(True)
""")

        with self.assertAddsMessages(
            Message(
                msg_id="legacy-return",
                node=call_node,
            ),
        ):
            self.checker.visit_call(call_node)

    def test_return_statement(self):
        call_node = astroid.extract_node("""\
return True
""")

        with self.assertNoMessages():
            self.checker.visit_call(call_node)
