# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback

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
from forms import *
from bacnet_control import *

@staff_member_required
def index(request):
	return render_to_response('bacnet/index.html', { }, context_instance=RequestContext(request))

@staff_member_required
def device_property(request, device_id, property_id):
	control = BacnetControl(settings.BACNET_BIN_DIR)
	try:
		value = control.read_analog_output(device_id, property_id)
	except:
		logging.exception('Could not read the analog output for bacnet device %s property %s' % (device_id, property_id))
		return HttpResponseServerError('Could not read the analog output for bacnet device %s property %s\n\n%s' % (device_id, property_id, sys.exc_info()[1]))

	device_property_form = DevicePropertyForm(data={'property_value':value})

	if request.method == 'POST':
		device_property_form = DevicePropertyForm(request.POST)
		if device_property_form.is_valid():
			new_value = device_property_form.cleaned_data['property_value']
			try:
				control.write_analog_output_int(device_id, property_id, int(new_value))
			except:
				logging.exception('Could not write the posted value (%s) for bacnet device %s property %s' % (new_value, device_id, property_id))
				return HttpResponseServerError('Could not write the posted value (%s) for bacnet device %s property %s\n\n%s' % (new_value, device_id, property_id, sys.exc_info()[1]))
			try:
				value = control.read_analog_output(device_id, property_id)
			except:
				logging.exception('Could not read the analog output for bacnet device %s property %s' % (device_id, property_id))
				return HttpResponseServerError('Could not read the analog output for bacnet device %s property %s\n\n%s' % (device_id, property_id, sys.exc_info()[1]))

	return render_to_response('bacnet/device_property.html', {'device_id':device_id, 'property_id':property_id, 'device_property_form':device_property_form}, context_instance=RequestContext(request))
