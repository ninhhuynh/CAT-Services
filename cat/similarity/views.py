
from similarity.dbfunctions import EditDistance
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from django.db.models import F, Func

from timeit import default_timer as timer
from django.db.models.expressions import Value
from django.db.models.fields import IntegerField, TextField
from django.http import response
from django.http.response import Http404
from rest_framework import generics, mixins, viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.response import Response


from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.serializers import HaystackSerializer
from rest_framework.serializers import Serializer
from six import Iterator

from similarity.search_indexes import SegmentPairIndex
from similarity.models import SegmentPair

from similarity.models import SegmentPair, Similarity, TranslationMemory
from similarity.serializers import TestSerializer, AdvanceSimilaritySerializer, NormalSimilaritySerializer, SegmentPairSerializer, SimilaritySerializer, TranslationMemorySerializer

# Create your views here.
import spacy
import timeit


similarityTool = spacy.load('en_core_web_md')
src = {}


def SetSource(data):
    global src
    src = similarityTool(data)


def Compare(tgt):
    global src
    tgt = similarityTool(tgt)
    return src.similarity(tgt)*100


@ api_view(['GET'])
@ permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'translation memory list': reverse('tm-list', request=request, format=format),
    })


class TMViewSet(viewsets.ModelViewSet):
    queryset = TranslationMemory.objects.all()
    serializer_class = TranslationMemorySerializer


class SegmentPairViewSet(viewsets.ModelViewSet):
    queryset = SegmentPair.objects.all()
    serializer_class = SegmentPairSerializer


class SimilarityList(generics.ListAPIView):
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer


class SimilarityViewSet(viewsets.ModelViewSet):
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer
    query_fields = ['src', 'tgt']

    @action(detail=False, permission_classes=[permissions.AllowAny])
    def get_similarity(self, request):
        queryset = self.get_queryset()
        queries = {}
        for field in self.query_fields:
            queries[field] = request.query_params.get(
                field)
            if not queries[field]:
                raise Http404()
        # if not queries['src']:
        #     raise Http404()

        start = timeit.default_timer()

        src = similarityTool(queries.get('src'))

        tgt = similarityTool(queries.get('tgt'))
        queries['similarity'] = src.similarity(tgt)*100
        obj = queryset.model.objects.create(**queries)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)


# class SearchView(HaystackViewSet):
#     queryset = SegmentPair.objects.all()
#     # `index_models` is an optional list of which models you would like to include
#     # in the search result. You might have several models indexed, and this provides
#     # a way to filter out those of no interest for this particular view.
#     # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
#     index_models = [SegmentPair]

#     serializer_class = SegmentPairSearchSerializer

#     permission_classes = [permissions.AllowAny]


# class AdvanceSimilaritySearchView(HaystackViewSet):
#     queryset = SegmentPair.objects.all()
#     # `index_models` is an optional list of which models you would like to include
#     # in the search result. You might have several models indexed, and this provides
#     # a way to filter out those of no interest for this particular view.
#     # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
#     index_models = [SegmentPair]

#     serializer_class = AdvanceSimilaritySerializer

#     permission_classes = [permissions.AllowAny]

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             request_doc = similarityTool(request.query_params['src'])

#             # Annotate pair with similairty to request sentence
#             for segment in page:
#                 segment.similarity = GetSimilarity(request_doc, segment.src)

#             serializer = self.get_serializer(
#                 page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(
#             queryset, many=True)
#         return Response(serializer.data)


class SearchView(mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = SegmentPair.objects.all()
    serializer_class = NormalSimilaritySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        query = request.query_params.get("q")
        if not query:
            return Response({"Bad Request": "Please specify a query string"})
        queryset = self.queryset.annotate(
            similarity=Func(F('src_segment'), Value(query), function='EDITDISTANCE', output_field=IntegerField()))
        queryset = queryset.filter(similarity__gt=0).order_by('-similarity')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True)
        return Response(serializer.data)


class VectorSimilaritySearchView(mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    queryset = SegmentPair.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        query = request.query_params.get("q")
        if not query:
            return Response({"Bad Request": "Please specify a query string"})

        queryset = self.queryset.annotate(
            similarity=Func(F('src_segment'), Value(query), function='EDITDISTANCE', output_field=IntegerField()))
        queryset = queryset.filter(similarity__gt=0)
        queryset = queryset.order_by('-similarity')[:100]

        SetSource(query)
        for x in queryset:
            x.vectorsimilarity = Compare(x.src_segment)
        queryset = list(queryset)
        queryset.sort(
            key=lambda object: -object.vectorsimilarity)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True)
        return Response(serializer.data)


def GetSimilarity(src, tgt):
    tgt = similarityTool(tgt)
    return src.similarity(tgt)*100


@ receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    connection.connection.create_function("EDITDISTANCE", 2, EditDistance)
    connection.connection.create_function("COMPARE", 1, Compare)
