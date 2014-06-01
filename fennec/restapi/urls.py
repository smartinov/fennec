from django.conf.urls import patterns, url, include
from rest_framework import routers
from dbsymbols.views import TableSymbolViewSet
from fennec.restapi.notifications.views import NotificationViewSet
from versioncontroll.views import GroupViewSet, UserViewSet, ProjectViewSet, BranchViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'table-symbols', TableSymbolViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
)