# Generated by Django 3.0.7 on 2022-03-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=1000)),
                ('type', models.IntegerField(default=0, max_length=2)),
                ('description', models.CharField(default=None, max_length=5000, null=True)),
                ('create_time', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAssets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('type', models.IntegerField(default=0, max_length=2)),
                ('severity', models.IntegerField(default=0, max_length=2)),
                ('ext', models.CharField(max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectIps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(max_length=10)),
                ('ips', models.CharField(max_length=200)),
                ('ext', models.CharField(max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectVuls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('vultype_id', models.IntegerField(max_length=10)),
                ('severity', models.IntegerField(default=0, max_length=2)),
                ('details', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=10)),
                ('nickname', models.CharField(max_length=30)),
                ('iphone', models.IntegerField(max_length=20)),
                ('score', models.IntegerField(default=0, max_length=2)),
                ('level', models.IntegerField(default=0, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='VulType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
