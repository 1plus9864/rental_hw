from django import forms
from .models import House
from .models import Appointment

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['title', 'location', 'price', 'room_type', 'size', 'description','image',]

        labels = {
            'title': '房源名稱',
            'location': '地區',
            'price': '租金',
            'room_type': '房型',
            'size': '坪數',
            'description': '房源介紹',
            'image': '房源照片',
        }
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ('renter', '租客'),
        ('landlord', '房東'),
    ]

    username = forms.CharField(label='帳號')

    password1 = forms.CharField(
        label='密碼',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='確認密碼',
        widget=forms.PasswordInput
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='身分'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'role'
        )
class AppointmentForm(forms.ModelForm):

    appointment_date = forms.DateField(
        label='預約日期',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Appointment

        fields = [
            'appointment_date',
            'message'
        ]

        labels = {
            'message': '留言',
        }

    class Meta:
        model = Appointment

        fields = [
            'appointment_date',
            'message'
        ]

        labels = {
            'appointment_date': '預約日期',
            'message': '留言',
        }