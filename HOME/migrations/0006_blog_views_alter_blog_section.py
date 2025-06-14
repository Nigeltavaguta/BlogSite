# Generated by Django 5.2.1 on 2025-05-13 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HOME', '0005_alter_blog_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blog',
            name='section',
            field=models.CharField(choices=[('Popular', 'Popular'), ('Trending', 'Trending'), ('Recent', 'Recent')], max_length=100),
        ),
    ]
