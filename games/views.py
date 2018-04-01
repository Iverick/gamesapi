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


# http://localhost:8000/game-categories/
class GameCategoryList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of GameCategory model objects
        and POST request creates an instance of GameCategory model.
    '''
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'


# http://localhost:8000/game-categories/<pk>/
class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of GameCategory model.
    '''
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'


# http://localhost:8000/games/
class GameList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of Game model objects and
        POST request creates an instance of Game model.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


# http://localhost:8000/games/<pk>/
class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of Game model.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'


# http://localhost:8000/players/
class PlayerList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of Player model objects and
        POST request creates an instance of Player model.
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


# http://localhost:8000/players/<pk>/
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of Player model.
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


# http://localhost:8000/player-scores/
class PlayerScoreList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of PlayerScore model objects
        and POST request creates an instance of PlayerScore model.
    '''
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'


# http://localhost:8000/player-scores/<pk>/
class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of PlayerScore model.
    '''
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


# http://localhost:8000/
class ApiRoot(generics.GenericAPIView):
    '''
    View creates an endpoint for the root of the API.
    Defines GET method that provides a response object with a descriptive name
        for the views and their URLs.
    '''
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(
                GameCategoryList.name,
                request=request
            ),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request)
        })
