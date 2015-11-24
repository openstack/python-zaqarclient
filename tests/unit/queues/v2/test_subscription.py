# Copyright (c) 2015 Catalyst IT Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from zaqarclient.tests.queues import subscriptions as sub
from zaqarclient.transport import http


class QueuesV2SubscriptionHttpUnitTest(sub.QueuesV2SubscriptionUnitTest):

    transport_cls = http.HttpTransport
    url = 'http://127.0.0.1:8888/v2'
    version = 2
