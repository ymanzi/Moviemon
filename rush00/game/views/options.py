from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ..models.buttons import Buttons
from ..models.save import SaveSlot
from ..structures.data import Data


class Options(View):

	def get(self, request):
		return render(request, "options/index.html", {
			"title": "Options",
			"menu_title": "Options",
			"enabled_buttons": [Buttons.START, Buttons.A, Buttons.B]
		})

	def post(self, request):
		if Buttons.A in request.POST:
			return HttpResponseRedirect(reverse('save'))
		elif Buttons.B in request.POST:
			return HttpResponseRedirect(reverse('home'))
		elif Buttons.START in request.POST:
			return HttpResponseRedirect(reverse('worldmap'))
		return self.get(request)


class Save(View):

	@staticmethod
	def get_selected_slot(slots, reset=False):
		selected_index = 0
		for index, slot in enumerate(slots):
			if slot.selected:
				selected_index = index
			if reset:
				slot.selected = False
		return selected_index

	def get(self, request):
		slots = SaveSlot.objects.all()
		slots[self.get_selected_slot(slots, reset=True)].selected = True
		for slot in slots:
			slot.save()
		return render(request, "options/save.html", {
			"title": "Save",
			"menu_title": "Save game",
			'slots': slots,
			"enabled_buttons": [Buttons.A, Buttons.B, Buttons.DOWN, Buttons.UP]
		})

	def post(self, request):
		slots = SaveSlot.objects.all()
		if Buttons.B in request.POST:
			self.get_selected_slot(slots, reset=True)
			for slot in slots:
				slot.save()
			return HttpResponseRedirect(reverse('options'))
		if Buttons.A in request.POST or Buttons.UP in request.POST or Buttons.DOWN in request.POST :
			selected_index = self.get_selected_slot(slots, reset=True)
			if Buttons.A in request.POST:
				slots[selected_index].free = False
				d = Data()
				slots[selected_index].loaded = True
				slots[selected_index].number_of_moviemons = len(d.available_movies) + len(d.moviedex)
				slots[selected_index].number_of_moviemons_captured = len(d.moviedex)
				slots[selected_index].file = f'slot{slots[selected_index].letter}_{slots[selected_index].number_of_moviemons_captured}_{slots[selected_index].number_of_moviemons}.mmg'
				slots[selected_index].save()
				d.dump_to_file(slots[selected_index].file)
			elif Buttons.UP in request.POST:
				if selected_index > 0:
					selected_index -= 1
			elif Buttons.DOWN in request.POST:
				if selected_index < len(slots) - 1:
					selected_index += 1
			slots[selected_index].selected = True
			for slot in slots:
				slot.save()
		enabled_buttons = [Buttons.B, Buttons.UP, Buttons.DOWN, Buttons.A]
		return render(request, "options/save.html", {
			"title": "Save",
			"menu_title": "Save game",
			'slots': slots,
			"enabled_buttons": enabled_buttons
		})


class Load(View):
	title = "Load"

	def get(self, request):
		slots = SaveSlot.objects.all()
		selected_index = self.get_selected_slot(slots, reset=True)
		loaded_index = self.get_loaded_slot(slots, reset=False)
		slots[selected_index].selected = True
		selectable_buttons = [Buttons.A, Buttons.B, Buttons.UP, Buttons.DOWN]
		if selected_index == 0:
			selectable_buttons.remove(Buttons.UP)
		if selected_index == 2:
			selectable_buttons.remove(Buttons.DOWN)
		if slots[selected_index].free:
			selectable_buttons.remove(Buttons.A)
		for slot in slots:
			slot.save()
		return render(request, "options/load.html", {
			"title": self.title,
			"menu_title": "Load game",
			"slots": slots,
			"select_on_loaded": selected_index == loaded_index,
			"enabled_buttons": selectable_buttons
		})

	@staticmethod
	def get_selected_slot(slots, reset=False):
		selected_index = 0
		for index, slot in enumerate(slots):
			if slot.selected:
				selected_index = index
			if reset:
				slot.selected = False
		return selected_index

	@staticmethod
	def get_loaded_slot(slots, reset=False):
		loaded_index = -1
		for index, slot in enumerate(slots):
			if slot.loaded:
				loaded_index = index
			if reset:
				slot.loaded = False
		return loaded_index

	def post(self, request):
		slots = SaveSlot.objects.all()
		if Buttons.B in request.POST:
			self.get_selected_slot(slots, reset=True)
			self.get_loaded_slot(slots, reset=True)
			for slot in slots:
				slot.save()
			return HttpResponseRedirect(reverse('home'))
		loaded_index = self.get_loaded_slot(slots, reset=False)
		if Buttons.A in request.POST:
			selected_index = self.get_selected_slot(slots, reset=False)
			self.get_loaded_slot(slots, reset=True)
			for slot in slots:
				slot.save()
			if loaded_index != -1 and loaded_index == selected_index:
				return HttpResponseRedirect(reverse('worldmap'))
			elif not slots[selected_index].free:
				d = Data()
				slots[selected_index].loaded = True
				d.load_from_save(slots[selected_index].file)
		else:
			selected_index = self.get_selected_slot(slots, reset=True)
			if Buttons.UP in request.POST:
				if selected_index > 0:
					selected_index -= 1
			elif Buttons.DOWN in request.POST:
				if selected_index < len(slots) - 1:
					selected_index += 1
			slots[selected_index].selected = True
		for slot in slots:
			slot.save()
		return self.get(request)
