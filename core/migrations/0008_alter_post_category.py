# Generated by Django 4.2.1 on 2023-06-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_category_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='posts', to='core.category'),
        ),
    ]