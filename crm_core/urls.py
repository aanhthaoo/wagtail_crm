from django.urls import path
from .views import dashboard_view, trigger_customer_ai_analysis

app_name = "crm_core"

urlpatterns = [
    # Giao diện Dashboard CRM
    path("dashboard/", dashboard_view, name="dashboard"),
    
    # API kích hoạt AI phân tích khách hàng (Hỗ trợ cả 2 alias URL)
    path(
        "api/customers/<int:customer_id>/analyze/",
        trigger_customer_ai_analysis,
        name="customer_analyze",
    ),
    path(
        "api/customers/<int:customer_id>/analyze-ai/",
        trigger_customer_ai_analysis,
        name="customer_ai_analysis",
    ),
]
