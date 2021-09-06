from django.urls import path

from .views.battle import Battle
from .views.home import Home
from .views.moviedex import Moviedex, Detail
from .views.options import Options, Save, Load
from .views.worldmap import Worldmap

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('worldmap', Worldmap.as_view(), name='worldmap'),
	path('battle/<str:moviemon_id>', Battle.as_view(), name='battle'),
	path('moviedex', Moviedex.as_view(), name='moviedex'),
	path('moviedex/<str:moviemon_id>', Detail.as_view(), name='detail'),
	path('options', Options.as_view(), name='options'),
	path('options/save_game', Save.as_view(), name='save'),
	path('options/load_game', Load.as_view(), name='load'),
]
