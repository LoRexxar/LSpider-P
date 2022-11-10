# Generated by Django 3.0.7 on 2022-11-07 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0009_auto_20220812_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackendLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
                ('log_text', models.TextField(null=True)),
                ('log_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
