import os
import shutil
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads catalog data from JSON and restores product images from fixtures to media/pics'

    def handle(self, *args, **kwargs):
        # 1. Load Data
        self.stdout.write(self.style.WARNING("Loading data from catalog_data.json..."))
        try:
            call_command('loaddata', 'catalog_data.json')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load data: {e}"))
            return

        # 2. Copy Images
        self.stdout.write(self.style.WARNING("Restoring images from fixtures/images/ to media/pics/..."))
        
        # Path definitions
        source_dir = os.path.join(settings.BASE_DIR, 'fixtures', 'images')
        
        # Ensure MEDIA_ROOT exists, handle if it's not set
        media_root = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))
        target_dir = os.path.join(media_root, 'pics')
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            self.stdout.write(f"Created directory: {target_dir}")
            
        if os.path.exists(source_dir):
            count = 0
            for filename in os.listdir(source_dir):
                src = os.path.join(source_dir, filename)
                dst = os.path.join(target_dir, filename)
                # Only copy files
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    count += 1
            self.stdout.write(self.style.SUCCESS(f"Successfully copied {count} images to {target_dir}"))
        else:
             self.stdout.write(self.style.ERROR(f"Source directory {source_dir} not found! Images could not be restored."))

        self.stdout.write(self.style.SUCCESS("Catalog setup complete."))
