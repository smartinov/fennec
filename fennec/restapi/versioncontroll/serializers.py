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


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        url = serializers.HyperlinkedIdentityField(view_name='project-detail', lookup_field='id')
        model = Project
        fields = ('url', 'id', 'name', 'description', 'created_by')


class BranchSerializer(serializers.ModelSerializer):

    #def restore_object(self, attrs, instance=None):
    #    return Branch(**attrs)

    class Meta:

        project_ref = serializers.HyperlinkedRelatedField(source='project_ref', view_name='project-detail', queryset=Project.objects.all(), lookup_field='id', slug_url_kwarg='id')

        model = Branch
        fields = ('url', 'id', 'name', 'description', 'project_ref')
        #fields = ('url', 'id', 'name', 'description', 'project_ref')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Change
        fields = ('url', 'id', 'content', 'object_type', 'object_code', 'change_type', 'is_ui_change', 'made_by')


class ChangeSerializerAlt(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = ('object_type', 'object_ref', 'change_type', 'made_by')