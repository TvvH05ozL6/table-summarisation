# Generated by Django 2.2.8 on 2021-12-07 16:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djongo.models.json
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OcularMovement',
            fields=[
                ('user', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('results', djongo.models.json.JSONField(default=[])),
                ('table_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SparqlEndpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('error', models.BooleanField()),
                ('checked_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('gs_type', models.CharField(choices=[('Limaye200', 'Limaye200'), ('T2D', 'T2D'), ('CTA', 'CTA'), ('CEA', 'CEA'), ('CPA', 'CPA'), ('NONE', 'None')], default='NONE', max_length=10)),
                ('file_name', models.TextField()),
                ('global_status', models.CharField(max_length=5)),
                ('process', djongo.models.json.JSONField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edit_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('header', models.TextField(default='')),
                ('num_cols', models.PositiveIntegerField(default=0)),
                ('num_rows', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Table_Datas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', djongo.models.json.JSONField()),
                ('data_original', djongo.models.json.JSONField()),
                ('data', djongo.models.json.JSONField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantistablex.Tables')),
            ],
        ),
        migrations.CreateModel(
            name='Table_Annotations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.TextField()),
                ('gs_type', models.CharField(choices=[('Limaye200', 'Limaye200'), ('T2D', 'T2D'), ('CTA', 'CTA'), ('CEA', 'CEA'), ('CPA', 'CPA'), ('NONE', 'None')], default='NONE', max_length=10)),
                ('data', models.TextField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantistablex.Tables')),
            ],
        ),
    ]