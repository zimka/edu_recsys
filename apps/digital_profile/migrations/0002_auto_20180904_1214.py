# Generated by Django 2.0.5 on 2018-09-04 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digital_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='digitalprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='digital_profile', to='context.Student'),
        ),
    ]