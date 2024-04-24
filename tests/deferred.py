# pylint: disable=missing-docstring
from twisted.internet import reactor, defer


def check_was_called():
    dfrd = do_thing(1, "hello")
    if dfrd.called:
        print(dfrd.was_called)  # [no-member]


@defer.inlineCallbacks
def do_thing(a: int, b: str):
    yield reactor.callLater(1, lambda: None)
    print(f"{b}: {a}")
