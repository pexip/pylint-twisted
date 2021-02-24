pylint-twisted
===============
Based on an original implementation by Jonny Yu ([jonnyyu/pylint-twisted](https://github.com/jonnyyu/pylint-twisted))

## About

`pylint-twisted` is [Pylint](http://pylint.org) plugin for improving code
analysis when editing code using [Twisted](http://flask.pocoo.org/).
Inspired by [pylint-django](https://github.com/landscapeio/pylint-django).

### Problems pylint-twisted solves:

1. Recognize generator with `defer.inlineCallbacks` decorator returns Deferred object.  Say you have the following code:

   ```python
    from twisted.internet import defer

    @defer.inlineCallbacks
    def func():
        yield some_other_func()

    def normal_deferred_func():
        d = foo()
        d.addCallback(lambda _: None)
        d.addErrback(lambda _: None)
   ```

   Normally, pylint will throw errors like:

   ```
    E:  1,0: No name 'addCallback' in generator 'func'
    E:  2,0: No name 'addErrback' in generator 'func'
   ```

   As pylint builds it's own abstract syntax tree, `pylint-twisted` will translate
   the `@defer.inlineCallbacks` decorator to return Deferred object instead of a generator, so pylint can continue
   checking your code.

2. Recognize `twisted.internet.reactor` module. Say you have the following code:

   ```python
    from twisted.internet import reactor

    def foo():    
        return reactor.seconds()
   ```

   Normally, pylint will throw errors like:

   ```
    E: 1,0: No name 'seconds' in module 'reactor'
   ```

   twisted reactor modules actually imports different modules base on the OS type at runtime.
   `pylint-twisted` will run the imports to let pylint know the actual reactor module, so pylint can continue
   checking your code.

## Usage

Ensure `pylint-twisted` is installed and on your path, and then run pylint using
pylint-twisted as a plugin.

```
pip install pylint-twisted
pylint --load-plugins pylint_twisted [..your module..]
```

## Contributing

Pull requests are always welcome.  Here's an outline of the steps you need to
prepare your code.

1. git clone https://github.com/pexip/pylint-twisted.git
2. cd pylint-twisted
3. mkvirtualenv pylint-twisted
4. pip install -r dev-requirements.txt
5. git checkout -b MY-NEW-FIX
6. Hack away
7. Make sure everything is green by running `tox`
7. git push origin MY-NEW-FIX
8. Create a pull request
