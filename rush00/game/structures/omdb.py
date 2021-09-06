import requests

from .moviemon import Moviemon


def get_movies(movies):
	moviemon = []
	for movie_id in movies:
		url = "http://www.omdbapi.com/?apikey=3a11964f"
		param = {'i': movie_id}
		try:
			result = requests.get(url, param).json()
			moviemon.append(Moviemon(
				title=result['Title'],
				imdb_id=result['imdbID'],
				rating=result['imdbRating'],
				poster=result['Poster'],
				director=result['Director'],
				year=result['Year'],
				synopsis=result['Plot'],
				actors=result['Actors']
			))
		except Exception as e:
			print(movie_id, " :", e)
			exit()
	return moviemon
