# Generated by Django 5.1.4 on 2025-01-14 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpt_api', '0003_remove_diary_num_diary_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='sticker_path',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
