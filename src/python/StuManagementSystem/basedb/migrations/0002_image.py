# Generated by Django 4.2.13 on 2024-06-16 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='img/')),
            ],
        ),
    ]
