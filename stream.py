#!/usr/bin/env python

API_BASE_URL = 'https://cybre.space'

import os
from getpass import getpass

from fediplay import register, login, stream

if not os.path.exists('clientcred.secret'):
    register(API_BASE_URL)

if not os.path.exists('usercred.secret'):
    email = input('Email: ')
    password = getpass('Password: ')
    login(API_BASE_URL, email, password)

def run():
    stream(API_BASE_URL)

