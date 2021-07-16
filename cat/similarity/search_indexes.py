from django.utils import timezone
from haystack import indexes
from similarity.models import SegmentPair


class SegmentPairIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(
        document=True, use_template=True)
    src = indexes.CharField(model_attr="src_segment")
    tgt = indexes.CharField(model_attr="tgt_segment")

    # @staticmethod
    # def prepare_autocomplete(obj):
    #     return " ".join((
    #         obj.src_segment, obj.tgt_segment
    #     ))

    def get_model(self):
        return SegmentPair

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created__lte=timezone.now()
        )
