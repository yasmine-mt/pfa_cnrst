# Generated by Django 4.2.3 on 2023-08-01 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Visiteur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('message', models.TextField()),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]