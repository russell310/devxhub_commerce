from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from apps.user.models import Admin, Customer

UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        role = instance.groups.first()
        rep['groups'] = GroupSerializer(instance=role).data if role else None
        return rep


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        user = super().update(instance, validated_data)
        return user


class AdminSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Admin


class CustomerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Customer
