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

from payloadclient.v1 import queue

from wildcard.test.test_data import utils


def data(TEST):
    TEST.queues = utils.TestDataContainer()

    queue_dict_1 = {
        'uuid': '1',
        'name': 'enabled queue',
        'description': 'enabled queue description',
        'disabled': False,
    }

    queue1 = queue.Queue(queue.QueueManager(None), queue_dict_1)
    TEST.queues.add(queue1)
