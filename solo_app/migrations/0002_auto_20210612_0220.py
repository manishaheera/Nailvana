# Generated by Django 2.2 on 2021-06-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solo_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='default.png', upload_to='images/'),
        ),
    ]
