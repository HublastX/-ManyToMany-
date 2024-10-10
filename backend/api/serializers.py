from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    _isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields=["id", "_id", "username", "email", "name", "isAdmin"]

    def get__id(self, obj):
        return obj.id
    
    def get__isAdmin(self, obj):
        return obj.is_staff
    
    def get__name(self, obj):
        name = obj.first_name
        
        if name == "" : 
            name=obj.email

        return name; 

class UserSerializerWithToken(UserSerializers):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields=["id", "_id", "username", "email", "name", "isAdmin", "token"]
    
    def get__token(self, obj):
        return obj.is_staff