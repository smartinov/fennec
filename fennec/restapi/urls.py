from django.conf.urls import patterns, url, include
from rest_framework import routers
from versioncontroll.views import GroupViewSet, UserViewSet, ProjectViewSet, BranchViewSet
from dbmodel.views import NamespaceViewSet, TableViewSet, ColumnViewSet
from dbsymbols.views import DiagramViewSet, LayerViewSet, TableSymbolViewSet, ColumnSymbolViewSet


router = routers.DefaultRouter()
##vsc
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'branches', BranchViewSet)
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
)
