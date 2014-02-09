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

from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from wildcard import api


class CreateSubscriberLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Subscriber")
    url = "horizon:project:subscribers:create"
    classes = ("ajax-modal", "btn-create")


class EditSubscriberLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:project:subscribers:update"
    classes = ("ajax-modal", "btn-edit")


class DeleteSubscribersAction(tables.DeleteAction):
    data_type_singular = _("Subscriber")
    data_type_plural = _("Subscribers")

    def delete(self, request, obj_id):
        api.ripcord.subscriber_delete(request, obj_id)


class SubscribersTable(tables.DataTable):

    username = tables.Column('username', verbose_name=_("Username"))
    email_address = tables.Column(
        'email_address',
        verbose_name=_("Email"),
        filters=[defaultfilters.urlize]
    )
    domain = tables.Column('domain', verbose_name=_("Domain"))
    rpid = tables.Column('rpid', verbose_name=_("Remote Party ID"))

    class Meta:
        name = "subscribers"
        verbose_name = _("Subscribers")
        row_actions = (EditSubscriberLink, DeleteSubscribersAction)
        table_actions = (CreateSubscriberLink, DeleteSubscribersAction)

    def get_object_id(self, datum):
        return datum.uuid
