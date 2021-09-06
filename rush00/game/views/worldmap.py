from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from random import randrange, choice

from ..structures.data import Data
from ..models.buttons import Buttons


class Worldmap(View):
	def random_moviemon(self, request, data):
		if not randrange(5):
			data.movieballs += 1
			data.save()
			messages.success(request, "You got a movieball")
			return HttpResponseRedirect(reverse('worldmap'))
		data.save()
		if not randrange(5) and len(data.available_movies) > 0:
			movie = choice(data.available_movies)
			id = movie.imdb_id
			return HttpResponseRedirect(reverse('battle', args=[id]))
		if len(data.available_movies) == 0:
			messages.success(request, "All The MovieMon have been caught !")
		return HttpResponseRedirect(reverse('worldmap', ))

	def get(self, request):
		data = Data()
		return render(request, "worldmap.html", {
			"title": "Worldmap",
			"map": data.get_map(),
			"width": str(600 / (data.grid_size[0])) + "px",
			"height": str(400 / (data.grid_size[1])) + "px",
			"enabled_buttons": [Buttons.SELECT, Buttons.START, Buttons.UP, Buttons.DOWN, Buttons.RIGHT, Buttons.LEFT],
			"movieballs": data.movieballs
		})

	def post(self, request):
		data = Data()
		
		if Buttons.DOWN in request.POST and data.player_position[1] + 1 < data.grid_size[1]:
			data.player_position = data.player_position[0], data.player_position[1] + 1
			return self.random_moviemon(request, data)
			
		elif Buttons.UP in request.POST and data.player_position[1] > 0:
			data.player_position = data.player_position[0], data.player_position[1] - 1
			return self.random_moviemon(request, data)

		elif Buttons.LEFT in request.POST and data.player_position[0] > 0:
			data.player_position = data.player_position[0] - 1, data.player_position[1]
			return self.random_moviemon(request, data)

		elif Buttons.RIGHT in request.POST and data.player_position[0] + 1 < data.grid_size[0]:
			data.player_position = data.player_position[0] + 1, data.player_position[1]
			return self.random_moviemon(request, data)

		elif Buttons.SELECT in request.POST:
			return HttpResponseRedirect(reverse('moviedex'))

		elif Buttons.START in request.POST:
			return HttpResponseRedirect(reverse('options'))
		
		return self.get(request)