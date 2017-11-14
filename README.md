pylint-twisted
===============

## About

`pylint-twisted` is [Pylint](http://pylint.org) plugin for improving code
analysis when editing code using [Twisted](http://flask.pocoo.org/).
Inspired by [pylint-django](https://github.com/landscapeio/pylint-django).

### Problems pylint-twisted solves:

1. Recognize `defer.inlineCallbacks` style imports.  Say you have the following code:

   ```python
    from flask.ext import wtf
    from flask.ext.wtf import validators

    class PostForm(wtf.Form):
        content = wtf.TextAreaField('Content', validators=[validators.Required()])
   ```

   Normally, pylint will throw errors like:

   ```
    E:  1,0: No name 'wtf' in module 'flask.ext'
    E:  2,0: No name 'wtf' in module 'flask.ext'
    F:  2,0: Unable to import 'flask.ext.wtf'
   ```

   As pylint builds it's own abstract syntax tree, `pylint-twisted` will translate
   the `flask.ext` imports into the actual module name, so pylint can continue
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

1. git clone https://github.com/jonnyyu/pylint-twisted.git
2. cd pylint-twisted
3. mkvirtualenv pylint-twisted
4. pip install -r dev-requirements.txt
5. git checkout -b MY-NEW-FIX
6. Hack away
7. Make sure everything is green by running `tox`
7. git push origin MY-NEW-FIX
8. Create a pull request

## License