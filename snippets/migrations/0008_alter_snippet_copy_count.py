# Generated by Django 3.2.6 on 2021-08-25 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0007_alter_snippet_copy_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='copy_count',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]