from django.conf.urls import patterns, url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'branches', views.BranchViewSet)
router.register(r'hello', views.TestViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
