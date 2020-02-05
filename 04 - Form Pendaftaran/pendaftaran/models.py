from django.db import models
from django.contrib.auth.hashers import make_password

from utils.validators import validate_noHp, validate_noHp_exist
from utils.parsing import parsing_noHp

class SignUp(models.Model):
    nama        = models.CharField(max_length=255)
    noHp        = models.CharField(max_length=20,
        validators=[validate_noHp, validate_noHp_exist]
    )
    password    = models.CharField(max_length=255)
    email       = models.CharField(max_length=255)
    tanggalLahir= models.DateField()

    KATEGORI = [
        ('PNP', 'Mahasiswa PNP'),
        ('UMUM', 'Umum')
    ]
    status      = models.CharField(max_length=20, choices=KATEGORI)

    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        # membuat password yang dihash dan disimpan ke tabel signup
        self.password = make_password(self.password)
        # parsing noHp if 628
        self.noHp = parsing_noHp(self.noHp)
        super().save()
