from setuptools import setup


setup(
    name='sync',
    install_requires=[
        'apscheduler',
        'Flask',
        'Flask-Admin',
        'flask-restx',
        'flask-login',

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
