# -*- coding: utf-8 -*-

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

from django import template
from django.utils.translation import ugettext_lazy as _  # noqa
from horizon import tables


class ServiceFilterAction(tables.FilterAction):
    def filter(self, table, services, filter_string):
        q = filter_string.lower()

        def comp(service):
            if q in service.type.lower():
                return True
            return False

        return filter(comp, services)


def get_stats(service):
    return template.loader.render_to_string('admin/services/_stats.html',
                                            {'service': service})


def get_enabled(service, reverse=False):
    options = ["Enabled", "Disabled"]
    if reverse:
        options.reverse()
    # if not configured in this region, neither option makes sense
    if service.host:
        return options[0] if not service.disabled else options[1]
    return None


class ServicesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_('Id'), hidden=True)
    name = tables.Column("name", verbose_name=_('Name'))
    service_type = tables.Column('__unicode__', verbose_name=_('Service'))
    host = tables.Column('host', verbose_name=_('Host'))
    enabled = tables.Column(get_enabled,
                            verbose_name=_('Enabled'),
                            status=True)

    class Meta:
        name = "services"
        verbose_name = _("Services")
        table_actions = (ServiceFilterAction,)
        multi_select = False
        status_columns = ["enabled"]
