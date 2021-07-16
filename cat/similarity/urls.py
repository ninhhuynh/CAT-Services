
from django import urls
from django.urls import path
from django.urls.conf import include
from similarity import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tm', views.TMViewSet)
router.register(r'search', views.SearchView, basename="tm-search")
router.register(r'similarity', views.SimilarityViewSet)
router.register(r'segment-pairs', views.SegmentPairViewSet,
                basename="segment-pairs-view")
router.register(r'vector-similarity-search', views.VectorSimilaritySearchView)
router.root_view_name = 'tm'

urlpatterns = [
    path('tm-api/', include(router.urls)),
]
