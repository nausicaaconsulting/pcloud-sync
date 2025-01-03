from setuptools import setup


setup(
    name='sync',
    install_requires=[
        'Flask',
        'Flask-Admin',
        'flask-restx',
        'flask-login',

        # ORM
        'Flask-SQLAlchemy',
        'SQLAlchemy',
        'Flask-Migrate',

        # Environment variable parsing
        'environs',

        # Run prod server
        'gunicorn',
    ],
    extras_require={
        'dev': [
        ]
    },
)
