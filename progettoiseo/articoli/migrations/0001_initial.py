# Generated by Django 5.1.8 on 2025-06-11 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articolo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(blank=True, max_length=50, null=True)),
                ('titolo', models.CharField(max_length=200)),
                ('testo', models.TextField()),
                ('data_pubblicazione', models.DateTimeField(auto_now_add=True)),
                ('immagine', models.ImageField(blank=True, null=True, upload_to='immagini_articoli/')),
                ('autori', models.ManyToManyField(db_table='articolo_autori', related_name='articoli', to='accounts.profiloutente')),
            ],
            options={
                'db_table': 'articoli',
                'ordering': ['-data_pubblicazione'],
            },
        ),
    ]
