import threading
import time
from django.apps import AppConfig



class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .views import update_free_equipment_status
        def run_background():
            while True:
                update_free_equipment_status()
                time.sleep(10)

        thread = threading.Thread(target=run_background, daemon=True)
        thread.start()
