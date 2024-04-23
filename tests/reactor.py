# pylint: disable=missing-docstring, wrong-import-position
from twisted.internet import reactor


def call_when_running():
    reactor.attr_error()  # [no-member]
    reactor.stop()


reactor.callWhenRunning(call_when_running)
reactor.run()
