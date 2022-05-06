from django.db.models.signals import post_migrate
from django.dispatch import receiver
from mantistablex.models import Tables
from mantistablex.process.utils.assets.assets import Assets
from mantistablex.process.utils.assets import importer


@receiver(post_migrate)
def on_init_db(**kwargs):

    filenames = Assets().list_files("experimental_tables")

    for filename in filenames:
        extension = filename[filename.rindex('.'):]
        name = filename[0:filename.rindex('.')]
        if not Tables.objects.filter(name=name).exists() and extension == '.json':
            content = Assets().get_asset(f"experimental_tables/{filename}")
            importer.load_table(name, filename, content)