# Generated by Django 3.2.6 on 2021-08-25 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_snippet_original_snippet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='original_snippet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='snippet_copies', to='snippets.snippet'),
        ),
    ]
