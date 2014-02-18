# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from wildcard import api


class CreateDomainLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Domain")
    url = "horizon:project:domains:create"
    classes = ("ajax-modal", "btn-create")


class EditDomainLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:project:domains:update"
    classes = ("ajax-modal", "btn-edit")


class DeleteDomainsAction(tables.DeleteAction):
    data_type_singular = _("Domain")
    data_type_plural = _("Domains")

    def delete(self, request, obj_id):
        api.ripcord.domain_delete(request, obj_id)


class DomainsTable(tables.DataTable):

    name = tables.Column('name', verbose_name=_("Name"))

    class Meta:
        name = "domains"
        verbose_name = _("Domains")
        row_actions = (
            EditDomainLink,
            DeleteDomainsAction,
        )
        table_actions = (
            CreateDomainLink, DeleteDomainsAction,
        )

    def get_object_id(self, datum):
        return datum.uuid
