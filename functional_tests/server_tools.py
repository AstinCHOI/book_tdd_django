from django.conf import settings

from . import secrets

from os import path
import subprocess


THIS_FOLDER = path.abspath(path.dirname(__file__))

def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            'fab',
            'create_session_on_server:email={}'.format(email),
            '--host={}'.format(host),
            '--hide=everything,status',
            '--password={}'.format(secrets.STAGING_PASSWORD),
        ],
        cwd=THIS_FOLDER
    ).decode().strip()

def reset_database(host):
    subprocess.check_call(
        ['fab', 'reset_database',
         '--host={}'.format(host),
         '--password={}'.format(secrets.STAGING_PASSWORD),
        ],
        cwd=THIS_FOLDER
    )