from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from organization.models import Team, User, UserProfile
from utils.wx_api import code2session


class TeamSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField(many=True, read_only=True)
    leader = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    userprofile = UserProfileSerializer(read_only=True)

    def create(self, validated_data):
        if validated_data.__contains__('groups'):
            validated_data.pop('groups')
        if validated_data.__contains__('user_permissions'):
            validated_data.pop('user_permissions')
        if validated_data.get('is_superuser'):
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if validated_data.__contains__('password'):
            raw_pwd = validated_data.pop('password')
            instance.set_password(raw_pwd)
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = '__all__'


class AdminUserListSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ['username', 'team', 'team_leader', 'first_name', 'last_name', 'userprofile']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields.pop('password')
        self.fields['js_code'] = serializers.CharField()

    def validate(self, attrs):
        res = code2session(attrs['js_code'])
        if res.__contains__('errcode'):
            raise ValidationError({"detail": res.get('errmsg')})
        try:
            user = User.objects.get(username=res.get('openid'))
        except User.DoesNotExist:
            user = User.objects.create_user(username=res.get('openid'), password=res.get('openid'))
        user.session_key = res.get('session_key')
        user.save()
        attrs['username'] = res.get('openid')
        attrs['password'] = res.get('openid')
        return super().validate(attrs)

