from django.urls import path
from translator import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root, name="mt"),
    path('trainedmodels/', views.TrainedModelList.as_view(),
         name='trained-model-list'),
    path('trainedmodels/<int:pk>/', views.TrainedModelDetail.as_view()),
    path('translations/<model_name>/<text>', views.translation.as_view()),
    path('targettranslations', views.TargetTranslationList.as_view(),
         name='tgt-translation-list'),
    path('translations/', views.translationList.as_view(), name='translation-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
