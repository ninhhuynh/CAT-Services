from django.core.exceptions import PermissionDenied
from translator.models import Snippet, TrainedModel, SourceTranslation, TargetTranslation
from translator.serializers import SourceTranslationSerializer, TargetTranslationSerializer, SnippetSerializer, TrainedModelSerializer
from translator.myTranslator import myTranslator

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from django.shortcuts import get_object_or_404


translators = {}


@ api_view(['GET'])
@ permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'trainedmodels': reverse('trained-model-list', request=request, format=format),
        'translations': reverse('translation-list', request=request, format=format),
        'tgttranslations': reverse('tgt-translation-list', request=request, format=format),
    })


class TrainedModelList(generics.ListCreateAPIView):
    queryset = TrainedModel.objects.all()
    serializer_class = TrainedModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrainedModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrainedModel.objects.all()
    serializer_class = TrainedModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class translationList(generics.ListAPIView):
    queryset = SourceTranslation.objects.all()
    serializer_class = SourceTranslationSerializer


class translation(generics.RetrieveAPIView):
    queryset = SourceTranslation.objects.all()
    serializer_class = SourceTranslationSerializer
    lookup_fields = ['text', 'model_name']

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {}
        for field in self.lookup_fields:
            filter_kwargs[field] = self.kwargs[field]
        try:
            obj = queryset.get(**filter_kwargs)
        except queryset.model.DoesNotExist:
            modelToUse = get_object_or_404(
                TrainedModel, name=filter_kwargs['model_name'])
            if modelToUse.name not in translators:
                translators[modelToUse.name] = myTranslator(
                    {
                        "models": [modelToUse.name]
                    })

            obj = queryset.model.objects.create(**filter_kwargs)

            result = translators[modelToUse.name].Translate(obj.text)[1][0]
            for i in range(translators[modelToUse.name].n_best):
                TargetTranslation.objects.create(
                    text=result[i], rank=i+1, src=obj)

            return obj

        return obj


class TargetTranslationList(generics.ListAPIView):
    queryset = TargetTranslation.objects.all()
    serializer_class = TargetTranslationSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
