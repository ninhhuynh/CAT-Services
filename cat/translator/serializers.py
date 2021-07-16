from rest_framework import serializers
from translator.models import Snippet, TrainedModel, SourceTranslation, TargetTranslation


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos']


class TrainedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainedModel
        fields = ['name', 'desc', 'src_lang', 'tgt_lang']


class TargetTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetTranslation
        fields = ["rank", "text"]


class SourceTranslationSerializer(serializers.ModelSerializer):
    targettranslation_set = TargetTranslationSerializer(many=True)

    class Meta:
        model = SourceTranslation
        fields = ['text', "model_name", 'targettranslation_set']
