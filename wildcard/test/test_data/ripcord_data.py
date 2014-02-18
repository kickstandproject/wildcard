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

from ripcordclient.v1 import domain
from ripcordclient.v1 import subscriber

from wildcard.test.test_data import utils


def data(TEST):
    TEST.subscribers = utils.TestDataContainer()
    TEST.project_domains = utils.TestDataContainer()

    subscriber_dict_1 = {
        'uuid': '1',
        'username': 'test username',
        'password': 'test password',
        'domain': 'example.com',
        'email_address': 'test@example.com',
        'rpid': 'test rpid',
    }

    subscriber1 = subscriber.Subscriber(
        subscriber.SubscriberManager(None), subscriber_dict_1
    )
    TEST.subscribers.add(subscriber1)

    domain_dict_1 = {
        'uuid': '1',
        'name': 'test name',
    }

    domain1 = domain.Domain(
        domain.DomainManager(None), domain_dict_1
    )
    TEST.project_domains.add(domain1)
