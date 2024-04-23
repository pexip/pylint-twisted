# pylint: disable=missing-docstring
from twisted.internet import reactor, defer


def check_was_called():
    dfrd = deferred()
    if dfrd.called:
        print(dfrd.was_called)  # [no-member]


@defer.inlineCallbacks
def deferred():
    yield reactor.callLater(1, lambda: None)
