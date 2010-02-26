from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import socket, select
import threading
import pprint
from lxml import etree

from bacnet.models import *

APP_PATH = '/bacnet'
API_PATH = '/api/bacnet'

class APITest(TestCase):
	def setUp(self):
		self.client = Client()
		
	def tearDown(self):
		pass

	def test_api_views(self):
		self.failUnlessEqual(0, 0)
		response = self.client.get('%s/device/01/' % (API_PATH))
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code)
		element = etree.fromstring(response.content)

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
