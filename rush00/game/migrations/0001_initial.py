# Generated by Django 3.2.4 on 2021-06-20 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SaveSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free', models.BooleanField(default=True)),
                ('selected', models.BooleanField(default=False)),
                ('loaded', models.BooleanField(default=False)),
                ('number_of_moviemons', models.IntegerField()),
                ('number_of_moviemons_captured', models.IntegerField()),
                ('file', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=10)),
                ('letter', models.CharField(default='', max_length=1)),
            ],
        ),
    ]