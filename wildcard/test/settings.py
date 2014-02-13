# -*- coding: utf-8 -*-
# Copyright (c) 2013 PolyBeacon, Inc.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from horizon.test.settings import *  # noqa

from wildcard import exceptions

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(TEST_DIR, '..'))

ROOT_URLCONF = 'wildcard.urls'
TEMPLATE_DIRS = (
    os.path.join(TEST_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'wildcard.context_processors.openstack',
)

INSTALLED_APPS = (
    'compressor',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_nose',
    'horizon',
    'openstack_auth',
    'wildcard',
    'wildcard.dashboards.admin',
    'wildcard.dashboards.project',
    'wildcard.dashboards.settings',
)

AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)

SITE_BRANDING = 'KickstandProject Dashboard'

HORIZON_CONFIG = {
    'dashboards': ('admin', 'settings'),
    'default_dashboard': 'admin',
    "password_validator": {
        "regex": '^.{8,18}$',
        "help_text": "Password must be between 8 and 18 characters."
    },
    'user_home': None,
    'exceptions': {
        'recoverable': exceptions.RECOVERABLE,
        'not_found': exceptions.NOT_FOUND,
        'unauthorized': exceptions.UNAUTHORIZED
    },
}

AVAILABLE_REGIONS = [
    ('http://localhost:5000/v2.0', 'local'),
    ('http://remote:5000/v2.0', 'remote'),
]

OPENSTACK_KEYSTONE_URL = "http://localhost:5000/v2.0"
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "Member"

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'test_domain'

OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_group': True,
    'can_edit_project': True,
    'can_edit_domain': True,
    'can_edit_role': True
}

KICKSTAND_PAYLOAD_BACKEND = True
KICKSTAND_RIPCORD_BACKEND = True

KICKSTAND_RANDOM_PASSWORD_LENGTH = 12
import string
KICKSTAND_RANDOM_PASSWORD_CHARS = string.ascii_letters + string.digits

LOGGING['loggers']['wildcard'] = {
    'handlers': ['test'],
    'propagate': False,
}

SECRET_KEY = None
SECRET_KEY = '2%frmi0l22k394o16mm2lmcrns*-#38#uban(^w-#c+4#k)@mt'

NOSE_ARGS = [
    '--nocapture',
    '--nologcapture',
    '--cover-package=wildcard',
    '--cover-inclusive',
    '--all-modules',
]

POLICY_FILES_PATH = os.path.join(ROOT_PATH, "conf")
POLICY_FILES = {
    'identity': 'keystone_policy.json',
}
