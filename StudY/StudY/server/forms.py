from django import forms
from bootstrap_datepicker.widgets import DatePicker
from .models import *

university_choices = []

for el in University.objects.filter(is_active=True):
    university_choices.append((el.pk, el.name))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите ФИО'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Введите эл почту'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    university = forms.ChoiceField(choices=university_choices, widget=forms.Select(attrs={'placeholder': 'Выберите ваш университет'}), required=False)
    faculty = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите ваш факультет'}),required=False)
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите вашу кафедру'}), required=False)
    course = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Введите ваш курс'}), min_value=0, max_value=4, required=False)
    group = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите вашу группу'}), required=False)
    vk_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите ссылку на ВК'}), required=False)
    telegram_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите ссылку на телеграмм'}), required=False)
    student_card = forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Загрузить картинку', 'class': 'tf-button upload-btn'}), required=False)


class UserAuthenticateForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class OrderCustomerForm(forms.Form):
    sub_order = forms.ChoiceField(
        label='Уточняем предмет',
        choices=[],
        widget=forms.Select(attrs={'placeholder': 'Выберите предмет', 'required': 'true'}))
    date_order = forms.DateField(label='Определяем дедлайн', widget=forms.DateInput(attrs={'placeholder': 'Введите дату', 'required': 'true'}))
    gar_order = forms.DateField(
    label='Определяем гарантийный срок',
    widget=DatePicker(options={
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'todayHighlight': True,
        'startDate': '0d',
        'endDate': '+30d',
        'clearBtn': False,
        }))

    price_order = forms.IntegerField(
        label='Уточняем цену за работу',
        min_value=100,
        max_value=10000,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите цену', 'required': 'true'})
    )

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super(OrderCustomerForm, self).__init__(*args, **kwargs)
        self.fields['sub_order'].choices = [(choice, choice) for choice in choices]