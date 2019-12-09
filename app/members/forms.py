from bootstrap_datepicker_plus import DatePickerInput
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
        widget=DatePickerInput()
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


# Forms for PID
class CreatePIDForm(forms.Form):
    # Pet name
    pet_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # Pet Pics Upload button
    pet_image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file btn',
                'style': 'background-color: #7f7b7c; color: white'
            }
        )
    )

    # Pet Birth date
    pet_birthdate = forms.DateField(
        widget=DatePickerInput()
    )

    # Pet Breed
    pet_breed = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    # Pet EntryNumber
    pet_entry = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # Pet noseprint
    pet_noseprint = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file btn',
                'style': 'background-color: #7f7b7c; color: white'
            }
        )
    )

    # initial value from view(user.public_key)
    owner_key = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True,
            }
        )
    )

    # Owner fingerprint
    owner_fingerprint = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file btn',
                'style': 'background-color: #7f7b7c; color: white'
            }
        )
    )

    # Vet Key
    vet_key = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # Owner Priavate key for signature
    owner_private_key = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


    # Pet Parents
    # 펫의 부모를 확실히 링크시키기 위한 기능
    # 구현은 가능하나 복잡해질 가능성 우려하여 제외
    # pet_parents1 = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Parents Asset ID',
    #         }
    #     )
    # )
    # pet_parents2 = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Parents Asset ID',
    #         }
    #     )
    # )

# ------- 이하 Pet transaction은 CREATE 시에는 자동 생성--------
    # Pet Transactions
    # Create 단계에서는 최초 생성 트랜잭션으로 고정값
    # pet_transaction = ''

    # initial value from view(datetime.now)
    # date_created = forms.DateTimeField(
    #     widget=forms.HiddenInput()
    # )
    # initial value from view(datetime.now)
    # date_updated = forms.DateTimeField(
    #     widget=forms.HiddenInput()
    # )