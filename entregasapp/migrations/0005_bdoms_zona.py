# Generated by Django 4.2.4 on 2024-02-05 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entregasapp', '0004_alter_bdoms_codigopostal'),
    ]

    operations = [
        migrations.AddField(
            model_name='bdoms',
            name='zona',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
