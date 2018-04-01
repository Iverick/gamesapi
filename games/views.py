# django imports
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# rest_framework import
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
# local imports
from .models import Game, GameCategory, Player, PlayerScore
from .serializers import GameSerializer, GameCategorySerializer,\
                         PlayerSerializer, PlayerScoreSerializer


class GameCategoryList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of GameCategory model objects and
        POST request creates an instance of GameCategory model.
    '''
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of GameCategory model.
    '''
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'


class GameList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of Game model objects and
        POST request creates an instance of Game model.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of Game model.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'


class PlayerList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of Player model objects and
        POST request creates an instance of Player model.
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of Player model.
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of PlayerScore model objects
        and POST request creates an instance of PlayerScore model.
    '''
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of PlayerScore model.
    '''
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'
