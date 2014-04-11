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
from django.core.mail import send_mail
from django import forms
from django.utils.translation import ugettext_lazy as _

from horizon.forms import SelfHandlingForm
from horizon import messages

from wildcard.api import keystone


class ForgotUsernameForm(SelfHandlingForm):

    email = forms.CharField()

    user = None

    def clean(self):
        cleaned_data = super(ForgotUsernameForm, self).clean()
        email = cleaned_data.get('email')
        if email:
            self.user = keystone.user_find(None, email=email)
            if not self.user:
                raise forms.ValidationError(
                    _("there is no user with such email")
                )
        return cleaned_data

    def handle(self, request, data):
        send_mail(
            _('username reminder'),
            _('your username is %s') % self.user.name,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
        )
        messages.success(
            request,
            _('your username was sent by email')
        )
        return True
