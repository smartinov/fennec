from rest_framework import serializers
from django.contrib.auth.models import User, Group

from fennec.restapi.versioncontroll.models import Project, Branch, Change, BranchRevision, Sandbox


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='id')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProjectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='project-detail', lookup_field='id')

    class Meta:
        model = Project
        created_by = serializers.HyperlinkedRelatedField(source='created_by', view_name='user-detail', queryset=User.objects.all(), lookup_field='id', slug_url_kwarg='id')
        fields = ('url', 'id', 'name', 'description', 'created_by')


class BranchSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='branch-detail', lookup_field='id')

    class Meta:
        model = Branch
        created_by = serializers.HyperlinkedRelatedField(source='created_by', view_name='user-detail', queryset=User.objects.all(), lookup_field='id', slug_url_kwarg='id')
        project_ref = serializers.HyperlinkedRelatedField(source='project_ref', view_name='project-detail', queryset=Project.objects.all(), lookup_field='id', slug_url_kwarg='project_id')

        fields = ('id', 'name', 'type', 'description', 'current_version', 'project_ref', 'created_by')
        #fields = ('id', 'name', 'type', 'description', 'current_version', 'project_ref', 'created_by')


class BranchRevisionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='branchrevision-detail', lookup_field='id')

    class Meta:
        model = BranchRevision
        branch_ref = serializers.HyperlinkedRelatedField(source='branch_ref', view_name='branch-detail', queryset=Branch.objects.all(), lookup_field='id', slug_url_kwarg='branch_id')

        fields = ('id', 'revision_number', 'previous_revision_ref', 'branch_ref')


class SandboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sandbox
        fields = ('id',)

class ChangeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    content = serializers.CharField()
    objectType = serializers.CharField(source="object_type")
    objectCode = serializers.CharField(source="object_code")
    changeType = serializers.IntegerField(source="change_type")
    isUIChange = serializers.BooleanField(source="is_ui_change")
    madeBy = serializers.IntegerField(source="made_by")

    class Meta:
        model = Change
        fields = ('id', 'content', 'objectType', 'objectCode', 'changeType', 'isUIChange')


class ChangeSerializerAlt(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = ('object_type', 'object_ref', 'change_type', 'made_by')

