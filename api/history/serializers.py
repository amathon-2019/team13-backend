from rest_framework import serializers

from apps.history.models import History


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = [
            'device',
            'is_active',
            'created',
            'updated',
        ]
