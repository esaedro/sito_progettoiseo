from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eventi", "0004_alter_evento_immagine"),
    ]

    operations = [
        migrations.AddField(
            model_name="evento",
            name="solo_data",
            field=models.BooleanField(default=False),
        ),
    ]
