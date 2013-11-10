# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

from horizon import exceptions
from horizon import forms
from horizon import messages

from semaphore import api


LOG = logging.getLogger(__name__)


class BaseQueueForm(forms.SelfHandlingForm):

    name = forms.CharField(label=_("Name"))
    description = forms.CharField(
        label=_("Description"),
        widget=forms.widgets.Textarea,
    )


class CreateQueueForm(BaseQueueForm):

    def handle(self, request, data):
        try:
            queue = api.payload.queue_create(request, **data)
            messages.success(
                request,
                _('Queue "%s" was successfully created.') % data['name']
            )
            return queue
        except Exception:
            exceptions.handle(request, _('Unable to create queue.'))


class UpdateQueueForm(BaseQueueForm):

    uuid = forms.CharField(label=_("UUID"), widget=forms.HiddenInput)

    def handle(self, request, data):
        uuid = data.pop('uuid')
        try:
            api.payload.queue_update(request, uuid, **data)
            messages.success(
                request,
                _('Queue has been updated successfully.')
            )
        except Exception:
            exceptions.handle(request, ignore=True)
            messages.error(request, _('Unable to update the queue.'))
        return True
