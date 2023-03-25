import django_filters as df
from .models import CarTypes
from django.forms.widgets import TextInput, NumberInput


class CarsTypesFilter(df.FilterSet):
    producer = df.CharFilter(field_name='producer', lookup_expr='contains',
                             widget=TextInput(attrs={'placeholder': 'Producer'}))
    fuel = df.ChoiceFilter(choices=CarTypes.FUEL_CHOICES, empty_label='-- Choose fuel --')
    gearbox = df.ChoiceFilter(choices=CarTypes.GEARBOX_CHOICES, empty_label='-- Choose gearbox --')
    drive = df.ChoiceFilter(choices=CarTypes.DRIVE_CHOICES, empty_label='-- Choose drive --')
    price = df.NumberFilter(lookup_expr='lte', widget=NumberInput(attrs={'placeholder': 'Max price'}))

    class Meta:
        model = CarTypes
        fields = ['producer', 'fuel', 'gearbox', 'drive', 'price']
