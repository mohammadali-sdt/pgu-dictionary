# Generated by Django 3.2 on 2022-08-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suggest',
            options={'permissions': [('view_active_suggestions', 'Can view acived suggestions')], 'verbose_name': 'Suggest', 'verbose_name_plural': 'Suggests'},
        ),
        migrations.AddField(
            model_name='suggest',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='suggest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
