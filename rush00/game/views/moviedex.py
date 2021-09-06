from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ..models.buttons import Buttons
from ..structures.data import Data


class Moviedex(View):

	def get(self, request):
		d = Data()
		print(len(d.available_movies))
		if len(d.moviedex) > 0:
			selected_index = self.get_selected_index(d.moviedex)
			d.moviedex[selected_index].selected = True
			d.save()
			enabled_buttons = [Buttons.SELECT, Buttons.UP, Buttons.DOWN, Buttons.A]
			if selected_index == 0:
				enabled_buttons.remove(Buttons.UP)
				liste = d.moviedex[:3]
			elif selected_index == len(d.moviedex) - 1:
				enabled_buttons.remove(Buttons.DOWN)
				liste = d.moviedex[-3:]
			else:
				liste = d.moviedex[(selected_index - 1):(selected_index + 2)]
		else:
			liste = []
			enabled_buttons = [Buttons.SELECT]
		return render(request, "moviedex/index.html", {
			"title": "Moviedex",
			'movies': liste,
			"enabled_buttons": enabled_buttons
		})

	def post(self, request):
		if Buttons.SELECT in request.POST:
			return HttpResponseRedirect(reverse('worldmap'))
		if Buttons.A in request.POST:
			d = Data()
			selected_index = self.get_selected_index(d.moviedex)
			id = d.moviedex[selected_index].imdb_id
			return HttpResponseRedirect(reverse('detail', args=[id]))
		if Buttons.UP in request.POST or Buttons.DOWN in request.POST:
			d = Data()
			selected_index = self.get_selected_index(d.moviedex)
			d.moviedex[selected_index].selected = False
			if Buttons.UP in request.POST and selected_index > 0:
				selected_index -= 1
			elif Buttons.DOWN in request.POST and selected_index < len(d.moviedex) -1:
				selected_index += 1
			d.moviedex[selected_index].selected = True
			d.save()
		return self.get(request)

	def get_selected_index(self, movies):
		for i, mov in enumerate(movies):
			if mov.selected:
				return i
		return 0


class Detail(View):
	def get(self, request, moviemon_id):
		d = Data()
		movie = None
		for m in d.moviedex:
			if m.imdb_id == moviemon_id:
				movie = m
				break
		return render(request, "moviedex/detail.html", {
			"title": "Detail",
			'movie': movie,
			"enabled_buttons": [Buttons.B]
		})

	def post(self, request, moviemon_id):
		if Buttons.B in request.POST:
			return HttpResponseRedirect(reverse('moviedex'))
		return self.get(request, moviemon_id)
