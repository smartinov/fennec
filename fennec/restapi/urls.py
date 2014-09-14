from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from rest_framework_nested import routers
from fennec.restapi.versioncontroll.views import BranchRevisionViewSet
from versioncontroll.views import GroupViewSet, UserViewSet, ProjectViewSet, BranchViewSet

router = routers.SimpleRouter()

router.register(r'projects', ProjectViewSet)

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project_id')
projects_router.register(r'branches', BranchViewSet)
##vsc

branches_router = routers.NestedSimpleRouter(projects_router, r'branches', lookup='branch_id')
branches_router.register(r'revisions', BranchRevisionViewSet)

router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'branch-revisions',  BranchRevisionViewSet)



urlpatterns = patterns('',
                    url(r'^', include(router.urls)),
                    url(r'^', include(projects_router.urls)),
                    url(r'^', include(branches_router.urls)),
                    #url(r'^projects/(?P<project_id>[^/]+)/branches/(?P<branch_id>[^/]+)/sandbox/$', SandboxView.as_view(), name='sandbox_view')



                       #url(r'^projects/(?P<id>\w[\w-]*)/$', ProjectViewSet.as_view(), name='project-detail'),
                       #url(r'^branches/$', BranchViewSet.as_view(), name='branch-list'),
                       #projects/(?P<project_id_id>[^/]+)/branches/(?P<branch_id_id>[^/]+)/revisions/(?P<id>[^/]+)/$ [name='branchrevision-detail']
)
