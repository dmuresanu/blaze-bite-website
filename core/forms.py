from django import forms
import datetime

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = None  # Defer model setting until initialization
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        from .models import MenuItem
        self._meta.model = MenuItem
        super().__init__(*args, **kwargs)


class BookingForm(forms.ModelForm):
    class Meta:
        model = None  # Defer model setting until initialization
        fields = ['full_name', 'email', 'phone_number', 'number_of_people', 'date', 'time', 'special_requests']

    def __init__(self, *args, **kwargs):
        from .models import Booking
        self._meta.model = Booking
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError('The reservation date cannot be in the past.')
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time < datetime.datetime.now().time():
            raise forms.ValidationError('The reservation time cannot be in the past.')
        return time


class StaffUserCreationForm(forms.ModelForm):
    class Meta:
        model = None  # Defer model setting until initialization
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        from django.contrib.auth.models import User
        self._meta.model = User
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            from .models import StaffProfile
            StaffProfile.objects.create(user=user)
        return user
