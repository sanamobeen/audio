from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("text_to_audio", "0003_audio_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audio",
            name="language",
            field=models.CharField(max_length=10),
        ),
    ]
