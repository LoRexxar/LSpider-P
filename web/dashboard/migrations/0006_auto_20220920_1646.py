# Generated by Django 3.0.7 on 2022-09-20 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20220906_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAnnouncement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(default='', max_length=200, null=True)),
                ('content', models.TextField(default='', null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
