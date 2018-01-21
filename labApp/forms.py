from django import forms
from . import models


# форма регистрации
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5,label='Логин',
                               widget=forms.TextInput(attrs={'placeholder': 'логин',
                                                          'class': 'form-control'}))
    password = forms.CharField(min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'пароль'}), label='Пароль', )
    password2 = forms.CharField(min_length=8,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'повторите пароль'}), label='Повторите ввод')
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'email'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Фамилия'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Имя'}))
    birthday = forms.DateField(label='День рождения', widget=forms.DateTimeInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Дата рождения'}))
    choices = (('м', 'мужской'), ('ж', 'женский'))
    sex = forms.ChoiceField(label='Пол',
                            widget=forms.RadioSelect(attrs={'class': 'radio'}), choices=choices)
    img = forms.FileField(label='Фото',
                          widget=forms.ClearableFileInput(attrs={'class': 'ask-signup-avatar-input'}),
                            required=False)


# форма авторизации
class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'логин',
                                                          'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'пароль'}), label='Пароль')


class ProdactForm(forms.Form):
    prodact_name = forms.CharField(min_length=5, max_length=30, label='Наименование товара')
    description = forms.CharField(min_length=1, max_length=255, label='Описание')
    price = forms.FloatField(disabled=True, label='Цена')
    img = forms.FileField(required=False, label='Фотография')

    class Meta:
        model = models.Prodact
        fields = ('prodact_name', 'description', 'price', 'img', 'category')


class OrderForm(forms.Form):
    user = forms.CharField(disabled='True', label='Покупатель',
                           widget=forms.TextInput(attrs={'class': "form-control", }))
    prodact = forms.CharField(disabled='True', label='Продукт',
                              widget=forms.TextInput(attrs={'class': "form-control", }))
    order_date = forms.DateTimeField(disabled='True', label='Дата заказа',
                                     widget=forms.DateTimeInput(
                                         attrs={'class': 'form-control'}))
    number = forms.IntegerField(label='Количество', initial=1,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    order_price = forms.FloatField(disabled='True', label='Стоимость заказа',
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ProdactAddForm(forms.ModelForm):
    prodact_name = forms.CharField(min_length=5, max_length=30, label='Наименование',
                                   widget=forms.TextInput(attrs={'placeholder': 'название',
                                                         'class': "form-control", }),)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                               'placeholder': 'описание',
                                                               'rows': 3,
                                                               'cols': 25,
                                                               'required': 'true',
                                                               'id': 'descriptionArea',
                                                               'oninput': 'productDescriptionValidate(event)',
                                                               'onblur': 'removeDescriptionTipOnBlur()',
                                                               'onfocus': 'productDescriptionValidate(event)'}),)
    price = forms.FloatField(label='Цена',  widget=forms.NumberInput(attrs={'placeholder': 'цена за единицу',
                                                               'class': 'form-control'}),)
    img = forms.FileField(label='Изображение', widget=forms.ClearableFileInput(attrs={'class': 'ask-signup-avatar-input'}),
                            required=False)

    class Meta:
        model = models.Prodact
        fields = ('prodact_name', 'description', 'price', 'img', 'category')
