import logging
import os
import json
import warnings
from flask import redirect, request, url_for

import flask_login as login
from flask_admin import Admin, BaseView, AdminIndexView, expose, helpers
from wtforms import form, fields, validators
from flask_admin.form import SecureForm

from sync import settings

# Chemin vers le fichier de configuration JSON
CONFIG_FILE = "config.json"
logger = logging.getLogger(__name__)

# Fonction pour lire et écrire dans le fichier JSON
def read_config():
    """Lire le fichier JSON."""
    if not os.path.exists(CONFIG_FILE):
        return {"synchros": []}
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def write_config(data):
    """Écrire dans le fichier JSON."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Formulaire pour gérer les synchronisations
class SyncForm(form.Form):
    type = fields.StringField('Type', validators=[validators.InputRequired()])
    login = fields.StringField('Login', validators=[validators.InputRequired()])
    password = fields.PasswordField('Password', validators=[validators.InputRequired()])
    local_folder = fields.StringField('Local Folder', validators=[validators.InputRequired()])

# Vue personnalisée pour gérer les synchronisations via Flask-Admin
class SyncAdminView(BaseView):
    form_base_class = SecureForm

    def is_accessible(self):
        return login.current_user.is_authenticated


    @expose('/')
    def index(self):
        """Afficher la liste des synchronisations."""
        config = read_config()
        print(f"Config loaded: {config}")
        return self.render('admin/sync_config.html', synchros=config["synchros"])

    @expose('/add', methods=['GET', 'POST'])
    def add(self):
        """Ajouter une synchronisation."""
        form = SyncForm(request.form)
        if request.method == 'POST' and form.validate():
            # Ajouter une nouvelle synchronisation au fichier JSON
            new_sync = {
                "type": form.type.data,
                "login": form.login.data,
                "password": form.password.data,
                "local_folder": form.local_folder.data
            }
            config = read_config()
            config["synchros"].append(new_sync)
            write_config(config)
            return redirect(url_for('.index'))
        return self.render('admin/sync_form.html', form=form)

    @expose('/delete/<int:index>', methods=['POST'])
    def delete(self, index):
        """Supprimer une synchronisation."""
        config = read_config()
        if 0 <= index < len(config["synchros"]):
            del config["synchros"][index]
            write_config(config)
        return redirect(url_for('.index'))

# Fonction pour enregistrer l'administration dans l'application principale
def register_admin(app):
    """Configurer Flask-Admin pour l'application principale."""
    init_login(app)
    admin = Admin(
        app,
        name="Sync",
        index_view=AdminIndexViewWithAuth(),
        base_template='admin/admin_master.html',
        template_mode="bootstrap3",
    )
    with warnings.catch_warnings():
        # Supprimer les avertissements inutiles
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        admin.add_view(SyncAdminView(name="Synchronizations", endpoint="sync_admin"))
    print("===============>Admin registered")


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
