import logging
from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Customer, InteractionHistory, Order
from .services.ai_service import analyze_customer

logger = logging.getLogger(__name__)


def dashboard_view(request):
    """
    View hiển thị Dashboard phân tích CRM nội bộ:
    - 4 thẻ thống kê: Tổng khách hàng, Điểm tiềm năng trung bình, Khách nguy cơ rời bỏ cao, Doanh số dự kiến.
    - Danh sách khách hàng với thông tin chi tiết và nút kích hoạt phân tích AI.
    """
    # 1. Tổng số khách hàng
    total_customers = Customer.objects.count()

    # 2. Điểm tiềm năng trung bình (tính trên các khách hàng đã có điểm)
    avg_score_data = Customer.objects.filter(ai_lead_score__isnull=False).aggregate(avg_score=Avg("ai_lead_score"))
    avg_lead_score = round(avg_score_data["avg_score"] or 0, 1)

    # 3. Số lượng khách có nguy cơ rời bỏ cao (ai_churn_risk = 'High')
    high_churn_count = Customer.objects.filter(ai_churn_risk__iexact="High").count()

    # 4. Doanh số dự kiến (tổng các đơn hàng trong giai đoạn Negotiation hoặc Won)
    forecast_revenue_data = Order.objects.filter(stage__in=["Negotiation", "Won"]).aggregate(total=Sum("amount"))
    forecast_revenue = forecast_revenue_data["total"] or 0

    # Danh sách toàn bộ khách hàng
    customers = Customer.objects.all().order_by("-created_at")

    context = {
        "total_customers": total_customers,
        "avg_lead_score": avg_lead_score,
        "high_churn_count": high_churn_count,
        "forecast_revenue": forecast_revenue,
        "customers": customers,
    }
    return render(request, "crm_core/dashboard.html", context)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def trigger_customer_ai_analysis(request, customer_id: int):
    """
    Endpoint kích hoạt phân tích AI cho một khách hàng cụ thể.
    - Lấy thông tin khách hàng và lịch sử tương tác.
    - Gọi AI service (Gemini) để phân tích lead score, sentiment, churn risk, summary, recommended action.
    - Cập nhật trực tiếp kết quả vào Database.
    """
    try:
        # 1. Lấy thông tin Customer
        customer = get_object_or_404(Customer, pk=customer_id)

        # 2. Lấy danh sách lịch sử tương tác liên quan
        interactions_qs = customer.interactions.all().order_by("created_at")
        interactions_data = [
            {
                "channel": i.channel,
                "content": i.content,
                "created_at": i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for i in interactions_qs
        ]

        # 3. Lấy danh sách đơn hàng liên quan
        orders_qs = customer.orders.all().order_by("-created_at")
        orders_data = [
            {
                "order_code": o.order_code,
                "amount": float(o.amount),
                "stage": o.stage,
                "close_date": str(o.close_date) if o.close_date else None,
            }
            for o in orders_qs
        ]

        # 4. Đóng gói thông tin khách hàng
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "company": customer.company,
            "status": customer.status,
            "created_at": customer.created_at.strftime("%Y-%m-%d %H:%M:%S") if customer.created_at else None,
        }

        # 5. Gọi AI Service phân tích dữ liệu
        ai_result = analyze_customer(
            customer_info=customer_data,
            interactions=interactions_data,
            orders=orders_data,
        )

        # Kiểm tra nếu dịch vụ AI trả về lỗi nghiêm trọng
        if "error" in ai_result and not ai_result.get("summary"):
            return JsonResponse(
                {"success": False, "message": f"Phân tích AI thất bại: {ai_result.get('error')}", "data": ai_result},
                status=500,
            )

        # 6. Cập nhật toàn bộ trường AI vào bản ghi Customer
        customer.ai_lead_score = ai_result.get("lead_score")
        customer.ai_sentiment = ai_result.get("sentiment", "")
        customer.ai_churn_risk = ai_result.get("churn_risk", "")
        customer.ai_summary = ai_result.get("summary", "")
        customer.ai_recommended_action = ai_result.get("recommended_action", "")
        customer.ai_demographics = ai_result.get("demographics", "")
        customer.ai_rfm_analysis = ai_result.get("rfm_analysis", "")
        customer.ai_engagement = ai_result.get("engagement", "")
        customer.ai_predictive = ai_result.get("predictive", "")
        customer.save(
            update_fields=[
                "ai_lead_score", "ai_sentiment", "ai_churn_risk",
                "ai_summary", "ai_recommended_action",
                "ai_demographics", "ai_rfm_analysis", "ai_engagement", "ai_predictive",
                "updated_at",
            ]
        )

        logger.info(f"Da cap nhat phan tich AI cho khach hang ID={customer.id} ({customer.name}).")

        # 7. Trả về JsonResponse đầy đủ
        return JsonResponse(
            {
                "success": True,
                "message": f"Phân tích AI cho khách hàng '{customer.name}' thành công!",
                "data": {
                    "customer_id": customer.id,
                    "name": customer.name,
                    "ai_lead_score": customer.ai_lead_score,
                    "ai_sentiment": customer.ai_sentiment,
                    "ai_churn_risk": customer.ai_churn_risk,
                    "ai_summary": customer.ai_summary,
                    "ai_recommended_action": customer.ai_recommended_action,
                    "ai_demographics": customer.ai_demographics,
                    "ai_rfm_analysis": customer.ai_rfm_analysis,
                    "ai_engagement": customer.ai_engagement,
                    "ai_predictive": customer.ai_predictive,
                },
            },
            status=200,
            json_dumps_params={"ensure_ascii": False},
        )

    except (Customer.DoesNotExist, Http404):
        return JsonResponse(
            {
                "success": False,
                "message": f"Không tìm thấy khách hàng với ID {customer_id}.",
            },
            status=404,
            json_dumps_params={"ensure_ascii": False},
        )
    except Exception as exc:
        logger.error(f"Lỗi hệ thống khi xử lý phân tích AI cho customer_id={customer_id}: {exc}", exc_info=True)
        return JsonResponse(
            {
                "success": False,
                "message": f"Lỗi máy chủ nội bộ: {str(exc)}",
            },
            status=500,
            json_dumps_params={"ensure_ascii": False},
        )
