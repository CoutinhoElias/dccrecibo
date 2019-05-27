from dal import autocomplete
from django.contrib.auth.models import User
import django_filters

from dccrecibo.core.models import Receipt


class ReceiptFilter(django_filters.FilterSet):
    author = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all(), widget=django_filters.ModelChoiceFilter)

    class Meta:
        model = Receipt
        fields = ['author', 'vehicle', 'chassis', 'color']