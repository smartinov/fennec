from rest_framework import serializers
from django.contrib.auth.models import User, Group

from fennec.restapi.dbmodel.models import Project, Branch, Change


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('url', 'id', 'name', 'description','created_by')


class BranchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Branch
        fields = ('url', 'id', 'name', 'description', 'project_ref')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Change
        fields = ('url', 'id', 'content', 'object_type', 'object_code', 'change_type', 'is_ui_change', 'made_by')


class ChangeSerializerAlt(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = ('object_type', 'object_ref', 'change_type', 'made_by')