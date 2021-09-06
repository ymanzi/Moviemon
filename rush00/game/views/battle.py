from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib import messages

from random import choice, randrange
from ..models.buttons import Buttons
from ..structures.data import Data


class Battle(View):
	def get(self, request, moviemon_id):
		d = Data()
		movie = d.get_movie_by_id(moviemon_id)
		enabled_button = [Buttons.A, Buttons.B]
		luck = 50 - (float(movie.rating) * 10) + (float(d.player_strength) * 5)
		if luck < 1:
			luck = 1
		elif luck > 90:
			luck = 90
		if d.battle_won:
			enabled_button.remove(Buttons.A)
		return render(request, "battle/index.html", {
			"data": d,
			'title': movie.title,
			'poster': movie.poster,
			'movies': movie,
			'luck': luck,
			'imdb_id': moviemon_id,
			"enabled_buttons": enabled_button
		})

	def post(self, request, moviemon_id):
		d = Data()
		if d.battle_won:
			return self.get('worldmap')
		for m in d.available_movies:
			if m.imdb_id == moviemon_id:
				movie = m
				break
		if Buttons.B in request.POST:
			d.battle_won = False
			d.save()
			return HttpResponseRedirect(reverse('worldmap'))
		if Buttons.A in request.POST:
			if d.movieballs == 0:
				messages.success(request, "You have no more movieballs !")
			else:
				d.movieballs -= 1
				luck = 50 - (float(movie.rating) * 10) + (float(d.player_strength) * 5)
				if luck < 1:
					luck = 1
				elif luck > 90:
					luck = 90
				if luck > randrange(0, 100):
					messages.success(request, "You caught it")
					d.available_movies.remove(movie)
					d.moviedex.append(movie)
					d.battle_won = True
					d.save()
					return  self.get(request, moviemon_id) # HttpResponseRedirect(reverse('battle'))   #REDIRIGER VERS BATTLE MAIS EN DESACTIVANT LE BOUTON A
				else:
					messages.error(request, "You missed !")
			d.save()
			return self.get(request, moviemon_id)
		return self.get(request, moviemon_id)


# class Detail(View):
# 	def get(self, request, moviemon_id):
# 		d = Data()
# 		movie = None
# 		for m in d.moviedex:
# 			if m.imdb_id == moviemon_id:
# 				movie = m
# 				break
# 		return render(request, "battle/detail.html", {
# 			"title": "Detail",
# 			'movie': movie,
# 			"enabled_buttons": [Buttons.B]
# 		})

# 	def post(self, request, moviemon_id):
# 		if Buttons.B in request.POST:
# 			return HttpResponseRedirect(reverse('moviedex'))
# 		return self.get(request, moviemon_id)