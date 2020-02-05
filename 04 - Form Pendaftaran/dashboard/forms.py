from django import forms
from utils.validators import validate_noHp
from .models import Notification

class ProfileForm(forms.Form):
    nama = forms.CharField(max_length=255)
    noHp = forms.CharField(
        max_length=20,
        label='No HP',
        validators=[validate_noHp],
    )
    email = forms.CharField(
        max_length=255,
        widget=forms.EmailInput()
    )
    tanggalLahir = forms.DateField(
        label='Tanggal Lahir'
    )

    KATEGORI = [
        ('PNP', 'Mahasiswa PNP'),
        ('UMUM', 'Umum')
    ]
    status = forms.CharField(\
        max_length=20,
        widget=forms.RadioSelect(
            choices=KATEGORI
            )
    )


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = (
            'title',
            'message',
            'is_confirm_message',
            'confirm_message',
        )

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_confirm_message': forms.CheckboxInput(
                attrs={
                    'data-toggle': 'collapse',
                    'data-target': '#confirmMessage',
                }
            ),
            'confirm_message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

