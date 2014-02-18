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
from django import http

from mox import IsA

from wildcard import api
from wildcard.test import helpers as test


INDEX_URL = reverse('horizon:project:domains:index')
CREATE_URL = reverse('horizon:project:domains:create')
UPDATE_URL = reverse('horizon:project:domains:update', args=[1])


def extract_data(domain):
    fields = [
        'name',
    ]
    return {f: getattr(domain, f) for f in fields}


class DomainTests(test.TestCase):

    @test.create_stubs({api.ripcord: ('domain_list',)})
    def test_index(self):
        api.ripcord.domain_list(
            IsA(http.HttpRequest)
        ).AndReturn(self.project_domains.list())
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'project/domains/index.html')
        domains = res.context['domains_table'].data
        self.assertItemsEqual(domains, self.project_domains.list())

    def _test_create_successful(self, domain, create_args, post_data):
        api.ripcord.domain_create(
            IsA(http.HttpRequest),
            **create_args
        ).AndReturn(domain)
        self.mox.ReplayAll()

        post_data['method'] = 'CreateDomainForm'
        res = self.client.post(CREATE_URL, post_data)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    def _test_update_successful(self, domain, update_args, post_data):
        api.ripcord.domain_get(
            IsA(http.HttpRequest),
            domain.uuid,
        ).AndReturn(domain)
        api.ripcord.domain_update(
            IsA(http.HttpRequest),
            domain.uuid,
            **update_args
        ).AndReturn(None)
        self.mox.ReplayAll()

        post_data['method'] = 'UpdateDomainForm'
        res = self.client.post(UPDATE_URL, post_data)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.ripcord: ('domain_create',)})
    def test_create(self):
        domain = self.project_domains.get(uuid='1')
        post_data = extract_data(domain)
        self._test_create_successful(
            domain,
            extract_data(domain),
            post_data,
        )

    @test.create_stubs({api.ripcord: ('domain_get', 'domain_update')})
    def test_update(self):
        domain = self.project_domains.get(uuid='1')
        post_data = extract_data(domain)
        post_data['uuid'] = domain.uuid
        self._test_update_successful(
            domain,
            extract_data(domain),
            post_data,
        )

    @test.create_stubs({api.ripcord: ('domain_delete', 'domain_list')})
    def test_delete(self):
        uuid = '1'
        api.ripcord.domain_delete(
            IsA(http.HttpRequest),
            uuid,
        )
        api.ripcord.domain_list(
            IsA(http.HttpRequest),
        ).AndReturn(self.project_domains.list())
        self.mox.ReplayAll()

        form_data = {'action': 'domains__delete__%s' % uuid}
        res = self.client.post(INDEX_URL, form_data)

        self.assertRedirectsNoFollow(res, INDEX_URL)
