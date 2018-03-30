# rest_framework import
from rest_framework import serializers
# local imports
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    '''
    GameSerializer.serializers

    Serializes the Game model of the games app.
    '''
    class Meta:
        model = Game
        fields = (
            'id',
            'created',
            'name',
            'release_date',
            'game_category',
            'played'
        )
