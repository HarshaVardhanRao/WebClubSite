# Generated by Django 5.1.5 on 2025-01-21 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_task_taskcompletion'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mentees', to='web.mentor'),
        ),
    ]
