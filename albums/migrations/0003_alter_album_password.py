# Generated by Django 5.1 on 2024-08-17 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_alter_albumimage_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='password',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
