from rest_framework import permissions, reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@ api_view(['GET'])
@ permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'machine-translation-services': reverse.reverse("mt", request=request, format=format),
        'translation-memory-services': reverse.reverse("tm", request=request, format=format),
    })
