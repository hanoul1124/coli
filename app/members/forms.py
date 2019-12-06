from django import forms

SEX_CHOICES = (('male', 'Male'), ('female', 'Female'))
AUTHORITIES_CHOICES = (
    ('Owner', 'Pet Owner'),
    ('Vet', 'Veterinarian'),
    ('Comp', 'Company')
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class SignupForm(forms.Form):
    # Public_key는 회원가입에서 표기하지 않으므로 제외한다.
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'firstDay': 1,
                'pattern=': '\d{4}-\d{2}-\d{2}',
                'lang': 'ko',
                'format': 'yyyy-mm-dd',
                'type': 'date'
            }
        )
    )
    sex = forms.ChoiceField(
            choices=SEX_CHOICES,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    authority = forms.ChoiceField(
            choices=AUTHORITIES_CHOICES,
    )