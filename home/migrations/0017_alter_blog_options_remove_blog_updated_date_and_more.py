# Generated by Django 5.1.4 on 2025-02-14 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_blog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={},
        ),
        migrations.RemoveField(
            model_name='blog',
            name='updated_date',
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogs/'),
        ),
    ]
