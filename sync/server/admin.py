import datetime

from flask import current_app, flash, redirect, request, url_for
import warnings
import logging

from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView

import flask_login as login

from wtforms import fields, form, validators

from sync import settings

logger = logging.getLogger(__name__)

# DEBUG
class FeaturesModelView(ModelView):
    can_delete = True
    can_view_details = True

    def is_accessible(self):
        return login.current_user.is_authenticated


class User:
    id = 1
    login = settings.ADMIN_LOGIN

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        if self.login.data != settings.ADMIN_LOGIN:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if self.password.data != settings.ADMIN_PASSWORD:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User()


class AdminIndexViewWithAuth(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        return self.render(self._template)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        login_form = LoginForm(request.form)
        if helpers.validate_form_on_submit(login_form):
            user = login_form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['login_form'] = login_form
        return super().index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(_user_id):
        return User()


def register_admin(app):
    init_login(app)
    admin = Admin(
        name="Stock listing",
        index_view=AdminIndexViewWithAuth(),
        base_template='admin_master.html',
        template_mode="bootstrap3",
    )
    with warnings.catch_warnings():
        # avoid warn when fields are excluded from a form
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        #admin.add_view(FeaturesModelView(models.Features, db.session))

        admin.init_app(app)
    # Root url should redirect to the admin
    app.add_url_rule('/', view_func=lambda: redirect(url_for('admin.index')))

    return
