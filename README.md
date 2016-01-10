# FormScribe
FormScribe is a Python 3 library intended to make form validation and processing both easy and correct. It's framework agnostic and test covered. It supports dynamic dependencies and post-validation actions through a declarative API, while using a minimal amount of magic.

### How can I install it?
Simply run `pip install formscribe`. The usage of a virtualenv is highly recommended.

### All right, what does it look like?
A simple login form may be implemented in just a few lines. The `submit` method specifies what should happen once the form is submitted.

HTML
```
<form role="form" method="post">
    <input name="username" type="text" value="" required>
    <input name="password" type="password" value="" required>
    <button type="submit">Log in</button>
</form>
```

Python, define the form using FormScribe in the 'forms' module
```
from formscribe import (Field, Form, ValidationError)
from some_login_implementation import do_login

class LoginForm(Form):
    class Username(Field):
        key = 'username'
        
        @staticmethod
        def validate(value):
            if not value:
                raise ValidationError("The username is mandatory.")
            return value

    class Password(Field):
        key = 'password'
        
        @staticmethod
        def validate(value):
            if not value:
                raise ValidationError("The password is mandatory.")
            if len(password) < 6:
                raise ValidationError("The password must be longer than 6 characters.")
            return value
    
    @staticmethod
    def submit(username, password):
        return do_login(username, password)
```

And then in your app, supposing you are using Flask:
```
from forms import LoginForm
import flask

@app.route('/login/', methods=["GET", "POST"])
def login():
    if flask.request.method == 'POST':
        loginform = LoginForm(flask.request.form)
        for error in loginform.errors:
            flask.flash(error.message)
        if not loginform.errors:
            flask.flash('You were successfully logged in.')
    else:
        return flask.render_template('login.html')
```

### You mentioned dynamic dependencies
It is possible to specify a given field should only be validated when another group of fields has also been validated, or when they have a certain value.
```
from formscribe import (Field, Form, ValidationError)

class CharacterManagement(Form):
    class Race(Field):
        key = 'race'
        
        @staticmethod
        def validate(value):
            if value not in ('elf', 'orc', 'human'):
                raise ValidationError("Invalid race.")
            return value
    
    class Clan(Field):
        key = 'clan'
        when_value = {'race': 'orc'}
        
        @staticmethod
        def validate(value):
            if clan not in ('Raz-bagdur', 'Kaz-faktur', 'Mak-sakur'):
                raise ValidationError('Invalid clan.')
            return value
```