from django.contrib.auth import authenticate
from rest_framework import serializers

from . import models as mo


class SignUp_Serializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    c_id = serializers.IntegerField()

    def create(self, validated_data):
        user = mo.User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"]
        )
        profile = mo.Profile(
            user=user,
            c_id=mo.Companys.objects.get(id=validated_data["c_id"])
        )

        user.save()
        profile.save()

        return user


# 로그인
class SignIn_Serializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to sign in with provided credentials.")


# Main Page
class MainDeviceList_Serialzier(serializers.ModelSerializer):
    class Meta:
        model = mo.Devices
        fields = ('id', 'name', 'connect', 'avgpm10', 'avgpm25')


class Total_AvgData_Serializer(serializers.ModelSerializer):
    class Meta:
        model = mo.AvgDatas
        fields = (
            'avgpm10', 'avgpm25'
        )


# Notice Page
class Notification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = mo.Notices
        fields = '__all__'


# Device setting Page
class DeviceSetting_Serializer(serializers.ModelSerializer):
    class Meta:
        model = mo.Devices
        fields = '__all__'


class AvgData_Serializer(serializers.ModelSerializer):
    class Meta:
        model = mo.AvgDatas
        fields = (
            'avgpm10', 'avgpm25'
        )


# Device Data Post
class DataPost_Serializer(serializers.ModelSerializer):
    pm10 = serializers.IntegerField()
    pm25 = serializers.IntegerField()
    d_id = serializers.IntegerField()

    class Meta:
        model = mo.RawDatas
        fields = '__all__'

    def create(self, validated_data):
        data = mo.RawDatas.objects.create(
            pm10=validated_data["pm10"],
            pm25=validated_data["pm25"],
            d_id=mo.Devices.objects.get(id=validated_data["d_id"])
        )
        return data
