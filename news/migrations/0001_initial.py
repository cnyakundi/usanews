# Generated by Django 4.0.1 on 2022-01-06 06:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField()),
                ('media_house_name', models.CharField(max_length=200)),
                ('image', models.URLField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('guid', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
    ]
