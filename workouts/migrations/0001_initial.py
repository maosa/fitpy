# Generated by Django 3.0.4 on 2020-04-11 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('workout', models.CharField(choices=[('Chest', 'Chest'), ('Back', 'Back'), ('Legs', 'Legs'), ('Compound', 'Compound'), ('Multisport', 'Multisport'), ('Running', 'Running'), ('Cycling', 'Cycling'), ('Bouldering', 'Bouldering'), ('Swimming', 'Swimming'), ('Surfing', 'Surfing'), ('Skiing', 'Skiing'), ('Other', 'Other'), ('Rest', 'Rest')], max_length=50)),
                ('duration', models.IntegerField()),
                ('distance', models.FloatField(blank=True, default=0, help_text='Only required for running workouts.')),
                ('pace', models.FloatField(blank=True)),
                ('category', models.CharField(blank=True, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
