# Generated by Django 3.1.5 on 2024-01-10 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamehive', '0007_auto_20231205_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameuserprofile',
            old_name='current_score_guess_number_game',
            new_name='current_score',
        ),
        migrations.RemoveField(
            model_name='gameuserprofile',
            name='current_score_rps',
        ),
    ]
