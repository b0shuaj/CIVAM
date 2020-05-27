# Generated by Django 2.2.6 on 2020-05-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='catalog_date',
            new_name='private_catalog_date',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='cataloger',
            new_name='private_cataloger',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='notes',
            new_name='private_notes',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='catalog_date',
            new_name='private_catalog_date',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='cataloger',
            new_name='private_cataloger',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='notes',
            new_name='private_notes',
        ),
        migrations.RenameField(
            model_name='personorinstitute',
            old_name='notes',
            new_name='private_notes',
        ),
        migrations.RemoveField(
            model_name='item',
            name='place_created',
        ),
        migrations.AddField(
            model_name='item',
            name='place_created',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
    ]