
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("text_to_audio", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="audio",
            old_name="title",
            new_name="text",
        ),
        migrations.AlterField(
            model_name="audio",
            name="audio_file",
            field=models.FileField(upload_to="generated/"),
        ),
    ]