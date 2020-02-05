# Generated by Django 2.2.9 on 2020-01-22 12:41

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('noHp', models.CharField(max_length=255)),
                ('lastLogin', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('noHp', models.CharField(max_length=20, validators=[utils.validators.validate_noHp])),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('tanggalLahir', models.DateField()),
                ('status', models.CharField(choices=[('PNP', 'Mahasiswa PNP'), ('UMUM', 'Umum')], max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]