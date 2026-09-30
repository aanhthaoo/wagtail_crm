import os
import sys
from django.apps import AppConfig


class CrmCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crm_core"

    def ready(self):
        # Print accessible routes when running development server
        is_runserver = any("runserver" in arg for arg in sys.argv)
        # Avoid printing twice due to Django autoreload process
        is_main_worker = os.environ.get("RUN_MAIN") == "true" or "--noreload" in sys.argv

        if is_runserver and is_main_worker:
            print("\n" + "=" * 68)
            print("   [CRM SYSTEM] HE THONG DA KHOI DONG THANH CONG!")
            print("=" * 68)
            print("   * CRM Dashboard (Chinh):  http://127.0.0.1:8000/crm/dashboard/")
            print("   * CRM Dashboard (Alias):  http://127.0.0.1:8000/dashboard/")
            print("   * Wagtail CMS Admin:      http://127.0.0.1:8000/admin/")
            print("   * Django Native Admin:    http://127.0.0.1:8000/django-admin/")
            print("   * AI Analyze API:         POST /api/customers/<id>/analyze/")
            print("=" * 68 + "\n")

