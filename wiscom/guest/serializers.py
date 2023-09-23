from rest_framework import serializers

from .models import Guest

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        # fields = ('name', 'comment')
        fields = '__all__'