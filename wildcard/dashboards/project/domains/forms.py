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

from horizon import exceptions
from horizon import forms
from horizon import messages

from wildcard import api


class BaseDomainForm(forms.SelfHandlingForm):

    name = forms.CharField(label=_("Name"))


class CreateDomainForm(BaseDomainForm):

    def handle(self, request, data):
        try:
            domain = api.ripcord.domain_create(request, **data)
            messages.success(
                request,
                _(
                    'Domain "%s" was successfully created.'
                ) % data['name']
            )
            return domain
        except Exception:
            exceptions.handle(request, _('Unable to create domain.'))


class UpdateDomainForm(BaseDomainForm):

    uuid = forms.CharField(
        label=_("UUID"),
        widget=forms.TextInput(attrs={'readonly': 'true'}),
    )

    def __init__(self, *args, **kwargs):
        super(UpdateDomainForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.remove('uuid')
        self.fields.keyOrder.insert(0, 'uuid')

    def handle(self, request, data):
        uuid = data.pop('uuid')
        try:
            api.ripcord.domain_update(request, uuid, **data)
            messages.success(
                request,
                _('Domain has been updated successfully.')
            )
        except Exception:
            exceptions.handle(request, ignore=True)
            messages.error(request, _('Unable to update the domain.'))
        return True
