# rest_framework import
from rest_framework import serializers
# local imports
from .models import Game, GameCategory, Player, PlayerScore
from . import views


class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    '''
    GameCategorySerializer.serializers

    Serializes instances of the GameCategory model of the games app.
    Games field used to display one to many relationships to objects of Game
        model.
    '''
    games = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='game-detail'
    )

    class Meta:
        model = GameCategory
        fields = ('url', 'pk', 'name', 'games')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    '''
    GameSerializer.serializers

    Serializes instances of the Game model of the games app.
    Game_category field used to show slugified list of instances of the
        GameCategory model. Instances of Game model have many to one
        relationship with instances of GameCategory model.
    '''
    game_category = serializers.SlugRelatedField(
        queryset=GameCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Game
        fields = (
            'url',
            'game_category',
            'name',
            'release_date',
            'played'
        )


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    '''
    ScoreSerializer.GameSerializer.serializers

    This serializer used to show all scores for a specific player.
    Created for use in PlayerSerializer.

    Game field used to display all details about the related game object.
    '''
    game = GameSerializer()

    class Meta:
        model = PlayerScore
        fields = ('url', 'pk', 'score', 'score_date', 'game')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    '''
    PlayerSerializer.ScoreSerializer.GameSerializer.serializers

    Serializes instances of the Player model.
    Scores field used to display all details about the related scores objects.
    (see above)
    '''
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Player.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True
    )

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores'
        )


class PlayerScoreSerializer(serializers.HyperlinkedModelSerializer):
    '''
    PlayerScoreSerializer.serializers

    Used to serialize instances of the PlayerScore model.
    '''
    player = serializers.SlugRelatedField(
        queryset=Player.objects.all(),
        slug_field='name'
    )
    game = serializers.SlugRelatedField(
        queryset=Game.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = PlayerScore
        fields = ('url', 'pk', 'score', 'score_date', 'player', 'game')
