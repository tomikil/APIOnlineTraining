# Generated by Django 5.0.7 on 2024-07-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_payment_payment_lesson_alter_payment_payment_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='город'),
        ),
    ]
