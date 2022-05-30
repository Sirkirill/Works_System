# Generated by Django 4.0.4 on 2022-05-30 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full name')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('iswc', models.CharField(blank=True, db_index=True, max_length=255, verbose_name='Iswc')),
                ('contributors', models.ManyToManyField(related_name='works', to='work.people', verbose_name='Contributors')),
            ],
        ),
    ]