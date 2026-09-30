from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import Customer, InteractionHistory, Order


class CustomerViewSet(SnippetViewSet):
    model = Customer
    icon = "user"
    menu_label = "Khách hàng"
    menu_name = "customers"
    add_to_admin_menu = False  # Được gom nhóm vào CRMViewSetGroup
    list_display = [
        "name",
        "email",
        "phone",
        "company",
        "status",
        "ai_lead_score",
        "ai_churn_risk",
        "created_at",
    ]
    list_filter = [
        "status",
        "ai_churn_risk",
        "created_at",
    ]
    search_fields = [
        "name",
        "email",
        "phone",
        "company",
    ]
    list_per_page = 20
    ordering = ["-created_at"]


class InteractionHistoryViewSet(SnippetViewSet):
    model = InteractionHistory
    icon = "history"
    menu_label = "Lịch sử tương tác"
    menu_name = "interactions"
    add_to_admin_menu = False  # Được gom nhóm vào CRMViewSetGroup
    list_display = [
        "customer",
        "channel",
        "content_preview",
        "created_at",
    ]
    list_filter = [
        "channel",
        "created_at",
    ]
    search_fields = [
        "customer__name",
        "customer__email",
        "content",
    ]
    list_per_page = 25
    ordering = ["-created_at"]


class OrderViewSet(SnippetViewSet):
    model = Order
    icon = "doc-full-inverse"
    menu_label = "Đơn hàng / Deal"
    menu_name = "orders"
    add_to_admin_menu = False  # Được gom nhóm vào CRMViewSetGroup
    list_display = [
        "order_code",
        "customer",
        "amount",
        "stage",
        "close_date",
        "created_at",
    ]
    list_filter = [
        "stage",
        "close_date",
        "created_at",
    ]
    search_fields = [
        "order_code",
        "customer__name",
        "customer__email",
    ]
    list_per_page = 20
    ordering = ["-created_at"]


class CRMViewSetGroup(SnippetViewSetGroup):
    menu_label = "Quản lý CRM"
    menu_icon = "group"
    menu_order = 200  # Vị trí trên sidebar Wagtail Admin
    items = (
        CustomerViewSet,
        InteractionHistoryViewSet,
        OrderViewSet,
    )


# Đăng ký nhóm ViewSet vào Wagtail Admin Menu
register_snippet(CRMViewSetGroup)
