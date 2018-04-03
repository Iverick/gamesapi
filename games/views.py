# django imports
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# django_filter imports
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter
# rest_framework import
from rest_framework import filters, generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
# local imports
from .models import Game, GameCategory, Player, PlayerScore
from .serializers import GameSerializer, GameCategorySerializer,\
                    PlayerSerializer, PlayerScoreSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


class PlayerScoreFilter(filters.FilterSet):
    '''
    Helper class used to add filtering properties for a PlayerScore model.
    '''
    min_score = NumberFilter(name='score', lookup_expr='gte')
    max_score = NumberFilter(name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(name='player__name')
    game_name = AllValuesFilter(name='game__name')

    class Meta:
        model = PlayerScore
        fields = (
            'score',
            'from_score_date',
            'to_score_date',
            # player__name will be accessed as player_name
            'player_name',
            # game__name will be accessed as game_name
            'game_name'
        )


# http://localhost:8000/game-categories/
class GameCategoryList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of GameCategory model objects
        and POST request creates an instance of GameCategory model.
    Throttle scope property defined at settings file of gamesapi project in
        REST_FRAMEWORK settings.
    '''
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


# http://localhost:8000/game-categories/<pk>/
class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of GameCategory model.
    Throttle scope property defined at settings file of gamesapi project in
        REST_FRAMEWORK settings.
    '''
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


# http://localhost:8000/games/
class GameList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of Game model objects and
        POST request creates an instance of Game model.
    perform_create method passes an additional owner field to the create
        method and sets the owner to the user received in the request.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    filter_fields = (
        'owner',
        'game_category',
        'name',
        'release_date',
        'played'
    )
    search_fields = ('^name',)
    ordering_fields = ('name', 'release_date')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# http://localhost:8000/games/<pk>/
class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of Game model.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


# http://localhost:8000/players/
class PlayerList(generics.ListCreateAPIView):
    '''
    View allows GET request retrieves a listing of Player model objects and
        POST request creates an instance of Player model.
    '''
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filter_fields = ('name', 'gender')
    search_fields = ('^name',)
    ordering_fields = ('name',)


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
    filter_fields = PlayerScoreFilter
    ordering_fields = ('score', 'score_date')


# http://localhost:8000/player-scores/<pk>/
class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View allows GET, PUT, PATCH and DELETE requests to retrieve, update and
        delete a specific instance of PlayerScore model.
    '''
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


# http://localhost:8000/users/
class UserList(generics.ListAPIView):
    '''
    View retrieves a list of users.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


# http://localhost:8000/users/<pk>/
class UserDetail(generics.RetrieveAPIView):
    '''
    View retrieves details about a specific user.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


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
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request)
        })
