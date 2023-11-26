# Generated by Django 4.2.1 on 2023-10-22 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_subcategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='blog.category'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='blog.tag'),
        ),
    ]
