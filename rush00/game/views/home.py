from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ..models.buttons import Buttons
from ..structures.data import Data


class Home(View):

	def get(self, request):
		return render(request, "home.html", {
			"title": "Homepage",
			"enabled_buttons": [Buttons.A, Buttons.B]
		})

	def post(self, request):
		if Buttons.A in request.POST:
			d = Data()
			d.load_default_settings()
			d.save()
			return HttpResponseRedirect(reverse('worldmap'))
		elif Buttons.B in request.POST:
			return HttpResponseRedirect(reverse('load'))
		return self.get(request)
