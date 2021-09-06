from django.apps import AppConfig


class GameConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'game'

	def ready(self):
		from .models.save import Saves
		# todo uncomment when pushing
		# Saves.charge_saves()
