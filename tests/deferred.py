# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from twisted.internet import reactor, defer


def check_was_called():
    dfrd = do_thing(1, "hello")
    if dfrd.called:
        print(dfrd.was_called)  # [no-member]

    yield Foo.why_would_you_do_this(True)
    yield Foo.just_no(False)


@defer.inlineCallbacks
def do_thing(a: int, b: str):
    yield reactor.callLater(1, lambda: None)
    print(f"{b}: {a}")


class Foo:

    @classmethod
    @defer.inlineCallbacks
    def why_would_you_do_this(cls, grrrr) -> None:
        yield defer.succeed(grrrr)

    @staticmethod
    @defer.inlineCallbacks
    def just_no(why) -> None:
        yield defer.succeed(why)
