# django imports
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# rest_framework import
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
# local imports
from .models import Game
from .serializers import GameSerializer


class JSONResponse(HttpResponse):
    '''
    Custom JSONResponse class extends django's HttpResponse response.
    Args:
        data: python object(dictionary)

    Adds to the constructor method following arguments:
        content: simple json string serialized from the given data
                 (which is simple python dictionary)
                 using JSONRenderer().render() method;
        content_type: adds 'application/json' value to the response header.
    '''
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


@csrf_exempt
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
        return JSONResponse(games_serializers.data)

    elif request.method == 'POST':
        '''
        Creates a new entry in the database.

        If request is POST view accepts given json string, serializes it.
        If values are valid view saves given data in database and returns
            saved data along with 201 code in response.
        If values not valid view sends 404 response along with raised errors.
        '''
        game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(data=game_data)

        if game_serializer.is_valid():
            game_serializer.save()
            return JSONResponse(
                game_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return JSONResponse(
                game_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@csrf_exempt
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
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        '''
        Extracts existing entry
        '''
        game_serializer = GameSerializer(game)
        return JSONResponse(game_serializer.data)

    elif request.method == 'PUT':
        '''
        Updates existing entry
        '''
        game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(game, data=game_data)

        if game_serializer.is_valid():
            game_serializer.save()
            return JSONResponse(game_serializer.data)

        return JSONResponse(
                game_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'DELETE':
        '''
        Deletes existing entry
        '''
        game.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
