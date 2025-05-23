from django.contrib.auth.models import User
from django.db import models

"""
Wechsel des user -> usernames von Einzigartig auf False , stadessen muss email einzigartig sein
"""
User._meta.get_field('username')._unique = False
User._meta.get_field('email')._unique = True