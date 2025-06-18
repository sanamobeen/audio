from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("text_to_audio", "0002_rename_title_audio_text_alter_audio_audio_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="audio",
            name="language",
            field=models.CharField(default="en", max_length=10),
        ),
    ]
