from rest_framework.viewsets import ModelViewSet

from dccrecibo.core.api.serializers import PersonSerializer
from dccrecibo.core.models import Person


class PersonViewSet(ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer