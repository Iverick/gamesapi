# django imports
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# rest_framework import
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
# local imports
from .models import Game
from .serializers import GameSerializer


@api_view(['GET', 'POST'])
def game_list(request):
    '''
    Returns list of the games or creates a new entry to database.
    '''
    if request.method == 'GET':
        '''
        Extracts all entries from the database.

        If request is GET view returns list of serialized database entries
        '''
        games = Game.objects.all()
        games_serializers = GameSerializer(games, many=True)
        return Response(games_serializers.data)

    elif request.method == 'POST':
        '''
        Creates a new entry in the database.

        If request is POST view accepts given json string, serializes it.
        If values are valid view saves given data in database and returns
            saved data along with 201 code in response.
        If values not valid view sends 404 response along with raised errors.
        '''
        game_serializer = GameSerializer(data=request.data)

        if game_serializer.is_valid():
            game_serializer.save()
            return Response(
                game_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
                game_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET', 'PUT', 'POST'])
def game_detail(request, pk):
    '''
    View used to access specific game from the database by given pk.
    Allows read, update and delete operations with database entries.

    Args:
        pk(int): 1
    '''
    try:
        game = Game.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        '''
        Extracts existing entry
        '''
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)

    elif request.method == 'PUT':
        '''
        Updates existing entry
        '''
        game_serializer = GameSerializer(game, data=request.data)

        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)

        return Response(
                game_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'DELETE':
        '''
        Deletes existing entry
        '''
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
