# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _  # noqa
import horizon


class SystemPanels(horizon.PanelGroup):
    slug = "admin"
    name = _("System Panel")
    panels = ('info',)


class IdentityPanels(horizon.PanelGroup):
    slug = "identity"
    name = _("Identity Panel")
    panels = ('domains', 'projects', 'users', 'groups', 'roles')


class Admin(horizon.Dashboard):
    name = _("Admin")
    slug = "admin"
    panels = (SystemPanels, IdentityPanels)
    permissions = ('openstack.roles.admin',)
    default_panel = 'users'


horizon.register(Admin)
