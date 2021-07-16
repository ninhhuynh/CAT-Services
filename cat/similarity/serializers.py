from similarity.search_indexes import SegmentPairIndex
from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, SerializerMethodField
from similarity.models import SegmentPair, TargetSimilarity, SourceSimilarity, Similarity, TranslationMemory


class TranslationMemorySerializer(serializers.ModelSerializer):
    # segmentpair_set = SegmentPairSerializer(many=True)

    class Meta:
        model = TranslationMemory
        fields = ['name', 'src_lang', 'tgt_lang']


class SegmentPairSerializer(serializers.ModelSerializer):
    src = TranslationMemorySerializer()

    class Meta:
        model = SegmentPair
        fields = ['src', 'src_segment', 'tgt_segment']


class TargetSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSimilarity
        fields = ['text', 'similarity']


class SourceSimilaritySerializer(serializers.ModelSerializer):
    targetsimilarity_set = TargetSimilaritySerializer(many=True)

    class Meta:
        model = SourceSimilarity
        fields = ['text', 'targetsimilarity_set']


class SimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Similarity
        fields = ['src', 'tgt', 'similarity']


class SegmentPairSearchSerializer(HaystackSerializer):

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [SegmentPairIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = ["src", "tgt"]


class AdvanceSimilaritySerializer(HaystackSerializer):
    similarity = SerializerMethodField()

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [SegmentPairIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = ["src", "tgt", 'similarity']

    def get_similarity(self, obj):
        return obj.similarity


class NormalSimilaritySerializer(serializers.ModelSerializer):
    similarity = serializers.IntegerField(default=-1)

    class Meta:
        model = SegmentPair
        fields = ['similarity', 'src_segment', 'tgt_segment']


class TestSerializer(serializers.ModelSerializer):
    similarity = serializers.IntegerField(default=-1)
    vectorsimilarity = serializers.IntegerField(default=-1)

    class Meta:
        model = SegmentPair
        fields = ['vectorsimilarity', 'similarity',
                  'src_segment', 'tgt_segment']
