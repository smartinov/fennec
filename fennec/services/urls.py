from django.conf.urls import patterns, url, include
from rest_framework import routers
from fennec.services.versioncontroll.views import BranchRevisionViewSet
from versioncontroll.views import GroupViewSet, UserViewSet, ProjectViewSet, BranchViewSet

router = routers.DefaultRouter()

router.register(r'projects', ProjectViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'branch-revisions', BranchRevisionViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),)
