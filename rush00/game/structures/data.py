import pickle
import random
from pathlib import Path

from django.conf import settings

from .omdb import get_movies


class Data:

	player_position = ()
	movieballs = 0
	moviedex = []
	available_movies = []
	grid_size = (0, 0)
	battle_won = False
	player_strength = len(moviedex)

	def __init__(self, file='data_dump.txt'):
		self.file = file
		if not Path('saves').exists():
			Path('saves').mkdir()
		self.free = not Path('saves/' + file).exists()
		if not self.free:
			try:
				with open('saves/' + file, 'rb') as file:
					obj = pickle.load(file)
					self.load(
						position=obj.player_position,
						player_strength=obj.player_strength,
						moviedex=obj.moviedex,
						available_movies=obj.available_movies,
						grid_size=obj.grid_size,
						movieballs=obj.movieballs,
						save=False
					)
			except Exception:
				print('Error loading the data from the file')
		else:
			self.load_default_settings()
			if file == 'data_dump.txt':
				self.save()

	def load_from_save(self, savefile):
		try:
			with open('saves/' + savefile, 'rb') as file:
				obj = pickle.load(file)
				self.load(
					position=obj.player_position,
					player_strength=obj.player_strength,
					moviedex=obj.moviedex,
					available_movies=obj.available_movies,
					grid_size=obj.grid_size,
					movieballs=obj.movieballs,
				)
		except Exception:
			print('Error loading the data to the file')

	def save(self):
		try:
			with open('saves/' + self.file, 'wb') as file:
				pickle.dump(self, file)
		except Exception:
			print('Error saving the data to the file')

	def load(self,
			save=True,
			position=None,
			available_movies=None,
			player_strength=None,
			moviedex=None,
			grid_size=None,
			movieballs=None):
		if position:
			self.player_position = position
		if available_movies:
			self.available_movies = available_movies
		if player_strength:
			self.player_strength = player_strength
		if moviedex:
			self.moviedex = moviedex
		if grid_size:
			self.grid_size = grid_size
		if movieballs:
			self.movieballs = movieballs
		if save:
			self.save()
		return self

	def dump(self):
		return self

	def get_random_movie(self):
		return self.available_movies[random.randint(0, len(self.available_movies) - 1)]

	def load_default_settings(self):
		self.available_movies = get_movies(settings.MOVIEMON_IDS)
		self.moviedex = []
		px, py = (settings.STARTING_POINT[0] - 1, settings.STARTING_POINT[1] - 1)
		gx, gy = settings.GRIDE_SIZE
		if gx < 10:
			gx = 10
		if gy < 10:
			gy = 10
		if px < 0:
			px = 0
		if py < 0:
			py = 0
		if px > gx - 1:
			px = gx - 1
		if py > gy - 1:
			py = gy - 1
		self.player_position = (px, py)
		self.grid_size = (gx, gy)

	def get_strength(self):
		return len(self.moviedex)

	def get_movie(self, name):
		for m in self.moviedex:
			if m.name == name:
				return m

	def get_movie_by_id(self, id):
		for m in self.moviedex:
			if m.imdb_id == id:
				return m
		for m in self.available_movies:
			if m.imdb_id == id:
				return m

	def get_map(self):
		map_ = [[False for w in range(self.grid_size[0]) ] for h in range(self.grid_size[1])]
		map_[self.player_position[1]][self.player_position[0]] = True
		return map_

	def dump_to_file(self, file):
		try:
			with open('saves/' + file, 'wb') as file:
				pickle.dump(self, file)
		except Exception:
			print('Error saving the data to the file')
