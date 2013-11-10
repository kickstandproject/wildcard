# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 NEC Corporation
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
import logging

from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import tables

from semaphore import api


LOG = logging.getLogger(__name__)


class CreateQueueLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Queue")
    url = "horizon:project:queues:create"
    classes = ("ajax-modal", "btn-create")


class EditQueueLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:project:queues:update"
    classes = ("ajax-modal", "btn-edit")


class ToggleEnabled(tables.BatchAction):
    name = "toggle"
    action_present = (_("Enable"), _("Disable"))
    action_past = (_("Enabled"), _("Disabled"))
    data_type_singular = _("Queue")
    data_type_plural = _("Queues")
    classes = ("btn-toggle",)

    def allowed(self, request, queue=None):
        if queue:
            self.disabled = queue.disabled
            self.current_present_action = int(not self.disabled)
        return True

    def action(self, request, obj_id):
        api.payload.queue_update(request, obj_id, disabled=not self.disabled)
        self.current_past_action = int(not self.disabled)


class DeleteQueuesAction(tables.DeleteAction):
    data_type_singular = _("Queue")
    data_type_plural = _("Queues")

    def delete(self, request, obj_id):
        api.payload.queue_delete(request, obj_id)


class QueuesTable(tables.DataTable):

    uuid = tables.Column("uuid", verbose_name=_("UUID"))
    name = tables.Column("name", verbose_name=_("Name"))
    created_at = tables.Column("created_at", verbose_name=_("Created At"))
    updated_at = tables.Column("updated_at", verbose_name=_("Updated At"))
    description = tables.Column("description", verbose_name=_("Description"))
    disabled = tables.Column("disabled", verbose_name=_("Disabled"))
    user_id = tables.Column("user_id", verbose_name=_("User"))
    project_id = tables.Column("project_id", verbose_name=_("Project"))

    class Meta:
        name = "queues"
        verbose_name = _("Queues")
        row_actions = (EditQueueLink, ToggleEnabled, DeleteQueuesAction)
        table_actions = (CreateQueueLink, DeleteQueuesAction)

    def get_object_id(self, datum):
        return datum.uuid
