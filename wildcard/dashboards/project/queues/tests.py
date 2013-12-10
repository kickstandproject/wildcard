# vim: tabstop=4 shiftwidth=4 softtabstop=4
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

from django.core.urlresolvers import reverse  # noqa
from django import http

from mox import IsA  # noqa

from wildcard import api
from wildcard.test import helpers as test


INDEX_URL = reverse('horizon:project:queues:index')
CREATE_URL = reverse('horizon:project:queues:create')
UPDATE_URL = reverse('horizon:project:queues:update', args=[1])


class QueueTests(test.TestCase):

    @test.create_stubs({api.payload: ('queue_list',)})
    def test_index(self):
        api.payload.queue_list(
            IsA(http.HttpRequest)
        ).AndReturn(self.queues.list())
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertTemplateUsed(res, 'project/queues/index.html')
        queues = res.context['queues_table'].data
        self.assertItemsEqual(queues, self.queues.list())

    def _test_create_successful(self, queue, create_args, post_data):
        api.payload.queue_create(
            IsA(http.HttpRequest),
            **create_args
        ).AndReturn(queue)
        self.mox.ReplayAll()

        post_data['method'] = 'CreateQueueForm'
        res = self.client.post(CREATE_URL, post_data)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    def _test_update_successful(self, queue, update_args, post_data):
        api.payload.queue_get(
            IsA(http.HttpRequest),
            queue.uuid,
        ).AndReturn(queue)
        api.payload.queue_update(
            IsA(http.HttpRequest),
            queue.uuid,
            **update_args
        ).AndReturn(None)
        self.mox.ReplayAll()

        post_data['method'] = 'UpdateQueueForm'
        res = self.client.post(UPDATE_URL, post_data)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.payload: ('queue_create',)})
    def test_create(self):
        queue = self.queues.get(uuid='1')
        self._test_create_successful(
            queue,
            {
                'name': queue.name,
                'description': queue.description,
            },
            {
                'name': queue.name,
                'description': queue.description,
            },
        )

    @test.create_stubs({api.payload: ('queue_create',)})
    def test_create_description_is_not_required(self):
        queue = self.queues.get(uuid='1')
        self._test_create_successful(
            queue,
            {
                'name': queue.name,
                'description': '',
            },
            {
                'name': queue.name,
            },
        )

    @test.create_stubs({api.payload: ('queue_get', 'queue_update')})
    def test_update(self):
        queue = self.queues.get(uuid='1')
        self._test_update_successful(
            queue,
            {
                'name': queue.name,
                'description': queue.description,
            },
            {
                'uuid': queue.uuid,
                'name': queue.name,
                'description': queue.description,
            },
        )

    @test.create_stubs({api.payload: ('queue_get', 'queue_update')})
    def test_update_description_not_required(self):
        queue = self.queues.get(uuid='1')
        self._test_update_successful(
            queue,
            {
                'name': queue.name,
                'description': '',
            },
            {
                'uuid': queue.uuid,
                'name': queue.name,
            },
        )

    @test.create_stubs({api.payload: ('queue_delete', 'queue_list')})
    def test_delete(self):
        uuid = '1'
        api.payload.queue_delete(
            IsA(http.HttpRequest),
            uuid,
        )
        api.payload.queue_list(
            IsA(http.HttpRequest),
        ).AndReturn(self.queues.list())
        self.mox.ReplayAll()

        form_data = {'action': 'queues__delete__%s' % uuid}
        res = self.client.post(INDEX_URL, form_data)

        self.assertRedirectsNoFollow(res, INDEX_URL)

    @test.create_stubs({api.payload: ('queue_update', 'queue_list')})
    def test_enable_queue(self):
        queue = self.queues.get(uuid="1")
        queue.disabled = True

        api.payload.queue_list(
            IsA(http.HttpRequest),
        ).AndReturn(self.queues.list())
        api.payload.queue_update(
            IsA(http.HttpRequest),
            queue.uuid,
            disabled=False
        ).AndReturn(None)

        self.mox.ReplayAll()

        formData = {'action': 'queues__toggle__%s' % queue.uuid}
        res = self.client.post(INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, INDEX_URL)

    @test.create_stubs({api.payload: ('queue_update', 'queue_list')})
    def test_disable_queue(self):
        queue = self.queues.get(uuid="1")
        queue.disabled = False

        api.payload.queue_list(
            IsA(http.HttpRequest),
        ).AndReturn(self.queues.list())
        api.payload.queue_update(
            IsA(http.HttpRequest),
            queue.uuid,
            disabled=True
        ).AndReturn(None)

        self.mox.ReplayAll()

        formData = {'action': 'queues__toggle__%s' % queue.uuid}
        res = self.client.post(INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, INDEX_URL)
