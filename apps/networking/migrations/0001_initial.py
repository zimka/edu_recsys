# Generated by Django 2.0.5 on 2018-09-21 11:37

import apps.core.models
import apps.core.raw_recommendation
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('context', '0007_student_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetenceNetworkingRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('source', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user_cmp', to='context.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='context.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.core.models.MutableMixin, models.Model, apps.core.raw_recommendation.RawRecommendation),
        ),
        migrations.CreateModel(
            name='ExperienceNetworkingRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('source', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user_exp', to='context.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='context.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.core.models.MutableMixin, models.Model, apps.core.raw_recommendation.RawRecommendation),
        ),
        migrations.CreateModel(
            name='InterestNetworkingRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('source', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user_int', to='context.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='context.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.core.models.MutableMixin, models.Model, apps.core.raw_recommendation.RawRecommendation),
        ),
    ]
