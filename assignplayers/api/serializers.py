from rest_framework import serializers
from players.models import PlayersDatastore, AppsList


class PlayersDatastoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayersDatastore
        fields = '__all__'
