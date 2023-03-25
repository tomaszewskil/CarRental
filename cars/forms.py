from django import forms
from .models import RentHistory, Car
from rentals.models import Rental
from stdnum.pl import pesel as checkPesel
from datetime import date


class RentHistoryForm(forms.ModelForm):
    pesel = forms.CharField()
    rental = forms.ModelChoiceField(queryset=Rental.objects.all())

    class Meta:
        model = RentHistory
        fields = ['start_date', 'end_date', 'add_fuel', 'pesel', 'rental']

    def __init__(self, car_type, *args, **kwargs):
        super(RentHistoryForm, self).__init__(*args, **kwargs)
        self.car_type = car_type
        self.fields['rental'].queryset = Rental.objects.filter(car__carType=self.car_type).distinct()
        self.fields['rental'].empty_label = '-- Choose rental --'
        self.fields['pesel'].widget = forms.TextInput(attrs={'placeholder': 'PESEL'})
        self.fields['start_date'].widget = forms.DateInput(attrs={'placeholder': 'Start date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'placeholder': 'End date'})

    def clean_pesel(self):
        pesel = self.cleaned_data['pesel']
        pesel = checkPesel.compact(pesel)
        if not checkPesel.is_valid(pesel):
            raise forms.ValidationError('PESEL is not valid!')
        birth_day = checkPesel.get_birth_date(pesel)
        today = date.today()
        age = today.year - birth_day.year - ((today.month, today.day) < (birth_day.month, birth_day.day))
        if age < 18:
            raise forms.ValidationError('You are to young to rent a car')

    def clean(self):
        super(RentHistoryForm, self).clean()
        clean_data = self.cleaned_data
        end_date = clean_data.get('end_date')
        start_date = clean_data.get('start_date')
        rental = clean_data.get('rental')

        if end_date and start_date:
            if start_date < date.today():
                raise forms.ValidationError("Start date is before today date")
            if end_date < start_date:
                raise forms.ValidationError("End date before start date")

            rented_cars = Car.objects.filter(renthistory__start_date__lte=end_date,
                                             renthistory__end_date__gte=start_date)

            available_cars = Car.objects.filter(rentals=rental, carType=self.car_type).difference(rented_cars)

            if not available_cars:
                raise forms.ValidationError("No available cars on this date")
