# vim: tabstop=4 shiftwidth=4 softtabstop=4
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

from django.core.urlresolvers import reverse

from wildcard import api
from wildcard.test import helpers as test


SPLASH_URL = reverse('splash')
FORGOT_USERNAME_URL = reverse('forgot-username')


class ForgotUsernameTests(test.TestCase):

    @test.create_stubs({api.keystone: ('user_find',)})
    def test_existent_email(self):
        user = self.users.get(id='1')
        api.keystone.user_find(
            None,
            email=user.email,
        ).AndReturn(user)
        self.mox.ReplayAll()

        formData = {
            'method': 'ForgotUsernameForm',
            'email': user.email,
        }
        res = self.client.post(FORGOT_USERNAME_URL, formData)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, SPLASH_URL)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.keystone: ('user_find',)})
    def test_nonexistent_email(self):
        user = self.users.get(id='1')
        api.keystone.user_find(
            None,
            email=user.email,
        ).AndReturn(None)
        self.mox.ReplayAll()

        formData = {
            'method': 'ForgotUsernameForm',
            'email': user.email,
        }
        res = self.client.post(FORGOT_USERNAME_URL, formData)

        self.assertFormErrors(res, count=0)
