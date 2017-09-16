# From: https://github.com/mbi/django-rosetta/issues/50
# Gunicorn may work with --reload option but it needs
# https://pypi.python.org/pypi/inotify package for performances

from django.dispatch import receiver
from rosetta.signals import post_save
from subprocess import Popen

import time
import os


@receiver(post_save)
def restart_server(sender, **kwargs):
    p = Popen(['./gunicorn.sh', 'restart'])
