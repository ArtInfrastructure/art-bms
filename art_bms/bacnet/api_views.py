# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback
import logging
import sys

from django.conf import settings
from django.db.models import Q
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.utils.html import strip_tags
import django.contrib.contenttypes.models as content_type_models
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import feedgenerator

from models import *
from art_bms.hydration import dehydrate_to_list_xml, dehydrate_to_xml
from bacnet_control import BacnetControl

class Device:
	"""Used to wrap the device"""
	def __init__(self, id):
		self.id = id
	class HydrationMeta:
		attributes = ['id']

def device(request, device_id):
	return HttpResponse(dehydrate_to_xml(Device(device_id)), content_type="text/xml")

def device_property(request, device_id, property_id):
	control = BacnetControl(settings.BACNET_BIN_DIR)
	if request.method == 'POST' and request.POST.get('value', None):
		new_value = request.POST.get('value', None)
		if new_value.isdigit():
			try:
				control.write_analog_output_int(device_id, property_id, int(new_value))
			except:
				logging.exception('Could not write the posted value (%s) for bacnet device %s property %s' % (new_value, device_id, property_id))
				return HttpResponseServerError('Could not write the posted value (%s) for bacnet device %s property %s\n\n%s' % (new_value, device_id, property_id, sys.exc_info()[1]))
		else:
			return HttpResponseServerError('Could not write the posted value (%s) for bacnet device %s property %s: unsupported value format' % (new_value, device_id, property_id))
			
	try:
		value = control.read_analog_output(device_id, property_id)
	except:
		logging.exception('Could not read the analog output for bacnet device %s property %s' % (device_id, property_id))
		return HttpResponseServerError('Could not read the analog output for bacnet device %s property %s\n\n%s' % (device_id, property_id, sys.exc_info()[1]))

	return HttpResponse(value, content_type="text/plain")

