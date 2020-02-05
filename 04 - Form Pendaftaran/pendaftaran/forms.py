from django import forms

from .models import SignUp
from utils.validators import validate_noHp

class LoginForm(forms.Form):
    noHp        = forms.CharField(
        label='No HP',
        widget=forms.TextInput(
            attrs={                
                'class': 'form-control',
                'placeholder': '08xxx',
            }
        ),
        validators=[validate_noHp]
    )
    password    = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = (
            'nama',
            'noHp',
            'password',
            'email',
            'tanggalLahir',
            'status'
        )
        # override default field
        labels = {
            'nama': 'Nama Lengkap',
            'noHp': 'No HP',
            'tanggalLahir': 'Tanggal Lahir',
        }

        widgets = {
            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'noHp': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '08xxx',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'tanggalLahir': forms.SelectDateWidget(
                attrs={
                    'class': 'form-control col-3',
                },
                years=range(1960, 2020, 1)
            ),
            'status': forms.RadioSelect(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }
