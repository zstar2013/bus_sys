# Generated by Django 2.0.3 on 2018-04-02 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.CharField(max_length=20)),
                ('route', models.CharField(max_length=20)),
                ('published_date', models.DateTimeField(verbose_name='date published')),
                ('updated_date', models.DateTimeField(verbose_name='date updated')),
                ('company', models.CharField(max_length=20)),
                ('team', models.CharField(choices=[('1', '1队'), ('2', '2队'), ('3', '3队'), ('4', '4队'), ('5', '5队')], max_length=10)),
                ('describe', models.CharField(max_length=50)),
                ('scrap', models.BooleanField()),
                ('car_num', models.CharField(default='', max_length=25)),
                ('en_num', models.CharField(default='', max_length=20)),
                ('cartype_value', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CarChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('change_value', models.CharField(max_length=50)),
                ('carInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_info.BusInfo')),
            ],
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subname', models.CharField(max_length=10)),
                ('company_name', models.CharField(max_length=20)),
                ('type_name', models.CharField(max_length=50)),
                ('power_type', models.CharField(choices=[('混', '油电混合'), ('柴', '柴油'), ('电', '纯电驱动'), ('汽', '汽油')], max_length=20)),
                ('car_length', models.CharField(max_length=10)),
                ('bus_load', models.IntegerField(default=0)),
                ('is_new_en', models.BooleanField()),
                ('car_scale', models.CharField(choices=[('大', '大型客车'), ('中', '中型客车'), ('小', '小型客车')], max_length=10)),
                ('target_value1', models.IntegerField(default=0)),
                ('target_value2', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='businfo',
            name='cartype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_info.CarType'),
        ),
    ]