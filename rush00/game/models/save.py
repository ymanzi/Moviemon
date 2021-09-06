from django.db import models

from ..structures.data import Data


class SaveSlot(models.Model):
	free = models.BooleanField(default=True)
	selected = models.BooleanField(default=False)
	loaded = models.BooleanField(default=False)
	number_of_moviemons = models.IntegerField()
	number_of_moviemons_captured = models.IntegerField()
	file = models.CharField(max_length=20, default='')
	name = models.CharField(max_length=10, default='')
	letter = models.CharField(max_length=1, default='')


class Saves:

	def load_save(self):
		pass

	@staticmethod
	def charge_saves():
		SaveSlot.objects.all().delete()
		slots = [
			Data(file='save0'),
			Data(file='save1'),
			Data(file='save2')
		]
		names = [
			'Slot A',
			'Slot B',
			'Slot C',
		]
		letters = [
			'a',
			'b',
			'c',
		]
		for i, slot in enumerate(slots):
			SaveSlot(
				selected=False,
				free=slot.free,
				number_of_moviemons=len(slot.available_movies) + len(slot.moviedex),
				number_of_moviemons_captured=len(slot.moviedex),
				file=slot.file,
				name=names[i],
				letter=letters[i]
			).save()
