# Generated by Django 2.1 on 2019-06-01 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_company'),
        ('accounts', '0002_auto_20190111_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradress',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.Company', verbose_name='Empresa'),
            preserve_default=False,
        ),
    ]
