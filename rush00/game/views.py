from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.conf import settings

from .models.buttons import Buttons
# from .structures.data import Data

from settings.BASE_DIR.structures import Data

def game_map(player_x, player_y):
	map_ = [[False for w in range(settings.GRIDE_SIZE[0]) ] for h in range(settings.GRIDE_SIZE[1])]
	map_[player_y][player_x] = True
	return map_

class Home(View):
	def get(self, request):
		return render(request, "home.html", {
			"title": "Homepage"
		})

	def post(self, request):
		if Buttons.A in request.POST:
		elif Buttons.B in request.POST:
			return HttpResponseRedirect(reverse('load'))

		return self.get(request)


class Worldmap(View):
	def get(self, request):
		data = Data()
		return render(request, "worldmap.html", {
			"title": "Worldmap",
			"map": game_map(data.player_position[0] ,  data.player_position[1])
		})


class Battle(View):
	def get(self, request):
		return render(request, "base.html", {
			"title": "Battle"
		})


class Moviedex(View):
	def get(self, request):
		return render(request, "base.html", {
			"title": "Moviedex"
		})


class Detail(View):
	def get(self, request):
		return render(request, "base.html", {
			"title": "Detail"
		})


class Options(View):
	def get(self, request):
		return render(request, "base.html", {
			"title": "Options"
		})


class Save(View):
	def get(self, request):
		return render(request, "base.html", {
			"title": "Save"
		})


class Load(View):
	def get(self, request):
		return render(request, "base.html", {
			"title": "Load"
		})
