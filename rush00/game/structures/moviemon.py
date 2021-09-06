class Moviemon:
	selected = False

	def __init__(self, title, imdb_id, rating=None, poster=None, director=None, year=None, synopsis=None, actors=None):
		self.title = title
		self.imdb_id = imdb_id
		self.rating = rating
		self.poster = poster
		self.director = director
		self.year = year
		self.synopsis = synopsis
		self.actors = actors

	def __str__(self):
		return self.title
