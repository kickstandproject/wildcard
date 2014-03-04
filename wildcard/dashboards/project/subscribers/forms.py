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

from django.conf import settings
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from wildcard import api


class TextInputWithGenerator(forms.TextInput):

    btn_classes = (
        'btn',
        'pull-right',
    )
    btn_label = _("Generate")

    def render(self, name, value, attrs=None):
        text_input = super(TextInputWithGenerator, self).render(
            name,
            value,
            attrs=attrs
        )
        return mark_safe(
            '<div class="input-with-button">%s <a%s>%s</a></div>' % (
                text_input,
                flatatt({
                    'class': ' '.join(self.btn_classes),
                    'data-chars': settings.KICKSTAND_RANDOM_PASSWORD_CHARS,
                    'data-length': settings.KICKSTAND_RANDOM_PASSWORD_LENGTH,
                }),
                self.btn_label,
            )
        )


class BaseSubscriberForm(forms.SelfHandlingForm):

    username = forms.CharField(label=_("Username"))
    password = forms.RegexField(
        label=_("Password"),
        regex=validators.password_validator(),
        error_messages={'invalid': validators.password_validator_msg()},
        widget=TextInputWithGenerator,
    )
    email_address = forms.EmailField(
        label=_("Email"),
        required=False,
    )
    domain_id = forms.ChoiceField(
        label=_("Domain"),
    )
    rpid = forms.CharField(
        label=_("Remote Party ID"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BaseSubscriberForm, self).__init__(*args, **kwargs)
        self.fields['domain_id'].choices = [
            (s.uuid, s.name)
            for s in api.ripcord.domain_list(self.request)
        ]


class CreateSubscriberForm(BaseSubscriberForm):

    @sensitive_variables('data')
    def handle(self, request, data):
        try:
            subscriber = api.ripcord.subscriber_create(request, **data)
            messages.success(
                request,
                _(
                    'Subscriber "%s" was successfully created.'
                ) % data['username']
            )
            return subscriber
        except Exception:
            exceptions.handle(request, _('Unable to create subscriber.'))


class UpdateSubscriberForm(BaseSubscriberForm):

    uuid = forms.CharField(
        label=_("UUID"),
        widget=forms.TextInput(attrs={'readonly': 'true'}),
    )
    password = forms.RegexField(
        required=False,
        label=_("Password"),
        regex=validators.password_validator(),
        error_messages={'invalid': validators.password_validator_msg()},
        widget=TextInputWithGenerator,
    )

    def __init__(self, *args, **kwargs):
        super(UpdateSubscriberForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.remove('uuid')
        self.fields.keyOrder.insert(0, 'uuid')

    @sensitive_variables('data')
    def handle(self, request, data):
        uuid = data.pop('uuid')
        data['password'] = data.get('password') or None
        try:
            api.ripcord.subscriber_update(request, uuid, **data)
            messages.success(
                request,
                _('Subscriber has been updated successfully.')
            )
        except Exception:
            exceptions.handle(request, ignore=True)
            messages.error(request, _('Unable to update the subscriber.'))
        return True
