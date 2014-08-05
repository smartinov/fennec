from django.conf.urls import patterns, url, include
from rest_framework_nested import routers
from versioncontroll.views import GroupViewSet, UserViewSet, ProjectViewSet, BranchViewSet, ChangeViewSet
from dbmodel.views import NamespaceViewSet, TableViewSet, ColumnViewSet
from dbsymbols.views import DiagramViewSet, LayerViewSet, TableSymbolViewSet, ColumnSymbolViewSet


router = routers.SimpleRouter()

router.register(r'projects', ProjectViewSet)

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='id')
projects_router.register(r'branches', BranchViewSet)
##vsc
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
#router.register(r'projects', ProjectViewSet)
#router.register(r'branches', BranchViewSet)
router.register(r'changes', ChangeViewSet)
#dbmodel
router.register(r'namespaces', NamespaceViewSet)
router.register(r'tables', TableViewSet)
router.register(r'columns', ColumnViewSet)

#symbols
router.register(r'diagrams', DiagramViewSet)
router.register(r'layers', LayerViewSet)
router.register(r'table-symbols', TableSymbolViewSet)
router.register(r'column-symbols', ColumnSymbolViewSet)

urlpatterns = patterns('',
                    url(r'^', include(router.urls)),
                    url(r'^', include(projects_router.urls))
                       #url(r'^projects/(?P<id>\w[\w-]*)/$', ProjectViewSet.as_view(), name='project-detail'),
                       #url(r'^branches/$', BranchViewSet.as_view(), name='branch-list'),
)
