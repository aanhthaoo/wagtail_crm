import json
import logging
from typing import Any, Dict, List, Optional
from django.conf import settings
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CustomerAnalysisOutput(BaseModel):
    # Tóm tắt tổng quan (hiển thị trên bảng)
    lead_score: int = Field(..., ge=1, le=100, description="Điểm tiềm năng 1-100")
    sentiment: str = Field(..., description="Positive / Neutral / Negative")
    churn_risk: str = Field(..., description="Low / Medium / High")
    summary: str = Field(..., description="Tóm tắt ngắn gọn 1-2 câu về tình trạng khách hàng")
    recommended_action: str = Field(..., description="Kết luận và hành động ưu tiên duy nhất cần thực hiện ngay")

    # Phân tích chi tiết theo 4 tiêu chí (hiển thị trong modal)
    demographics: str = Field(
        ...,
        description=(
            "Phân tích Thuộc tính định danh (Demographics/Firmographics): "
            "quy mô công ty, ngành nghề, vị trí địa lý, vai trò và cấp bậc của người đại diện ra quyết định. "
            "Đánh giá ICP (Ideal Customer Profile) fit và mức độ phù hợp với thị trường mục tiêu."
        ),
    )
    rfm_analysis: str = Field(
        ...,
        description=(
            "Phân tích hành vi giao dịch theo mô hình RFM: "
            "Recency (thời điểm giao dịch hoặc liên hệ gần nhất), "
            "Frequency (tần suất mua hàng/tương tác), "
            "Monetary (tổng giá trị đơn hàng đã đóng hoặc đang đàm phán). "
            "Phân loại phân khúc RFM (VIP/Loyal/At Risk/Lost)."
        ),
    )
    engagement: str = Field(
        ...,
        description=(
            "Phân tích mức độ tương tác và sắc thái cảm xúc (Engagement & Sentiment): "
            "tần suất phản hồi qua email/điện thoại, số lượng và tính chất của ticket hỗ trợ, "
            "xu hướng cảm xúc tích cực/tiêu cực qua nội dung trao đổi, "
            "chỉ số NPS ước tính và mức độ quan tâm đến sản phẩm/dịch vụ."
        ),
    )
    predictive: str = Field(
        ...,
        description=(
            "Phân tích các chỉ số dự đoán và vòng đời (Predictive Metrics): "
            "xác suất chuyển đổi (Lead Score chi tiết), vị trí hiện tại trong phễu bán hàng, "
            "nguy cơ rời bỏ (Churn Risk với lý do cụ thể), "
            "giá trị vòng đời dự kiến (CLV - Customer Lifetime Value), "
            "và thời điểm tối ưu để tiếp cận chốt đơn."
        ),
    )


def _get_fallback_response(error_message: str = "") -> Dict[str, Any]:
    return {
        "lead_score": 50,
        "sentiment": "Neutral",
        "churn_risk": "Medium",
        "summary": "Không thể phân tích lúc này do lỗi kết nối AI.",
        "recommended_action": "Kiểm tra lại cấu hình API key hoặc thử lại sau.",
        "demographics": "",
        "rfm_analysis": "",
        "engagement": "",
        "predictive": "",
        "error": error_message,
    }


def analyze_customer(
    customer_info: Dict[str, Any],
    interactions: Optional[List[Dict[str, Any]]] = None,
    orders: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Phân tích thông tin khách hàng theo 4 tiêu chí chuyên sâu bằng Google GenAI SDK.

    Args:
        customer_info: Thông tin cơ bản của khách hàng.
        interactions: Danh sách lịch sử tương tác.
        orders: Danh sách đơn hàng/deal của khách hàng.

    Returns:
        Dict gồm tóm tắt tổng quan và 4 phân tích chuyên sâu.
    """
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if not api_key:
        logger.warning("GEMINI_API_KEY chua duoc cau hinh.")
        return _get_fallback_response("GEMINI_API_KEY is missing")

    if interactions is None:
        interactions = []
    if orders is None:
        orders = []

    context_payload = {
        "customer": customer_info,
        "interactions": interactions,
        "orders": orders,
    }

    system_instruction = (
        "Bạn là một Chuyên gia phân tích dữ liệu CRM cấp cao (Senior CRM Intelligence Analyst) "
        "với chuyên môn sâu về B2B Sales, Customer Success và Predictive Analytics. "
        "Nhiệm vụ của bạn là phân tích toàn diện hồ sơ khách hàng dựa trên dữ liệu thực tế được cung cấp "
        "và đưa ra đánh giá chuyên sâu, có chiều sâu theo 4 tiêu chí khung phân tích:\n\n"
        "1. Demographics/Firmographics: Đặc điểm định danh công ty và người ra quyết định.\n"
        "2. RFM Model: Hành vi giao dịch và phân khúc giá trị khách hàng.\n"
        "3. Engagement & Sentiment: Mức độ gắn kết và xu hướng cảm xúc.\n"
        "4. Predictive Metrics: Chỉ số dự đoán tương lai và giá trị vòng đời.\n\n"
        "Ngoài 4 tiêu chí chi tiết, cần cung cấp phần TÓM TẮT TỔNG QUAN ngắn gọn (1-2 câu) "
        "và MỘT hành động ưu tiên cụ thể nhất cần thực hiện ngay. "
        "Phân tích phải dựa trên dữ liệu thực tế, có lập luận rõ ràng và bằng TIẾNG VIỆT. "
        "PHẢI tuân thủ JSON schema nghiêm ngặt."
    )

    # Danh sách model theo thứ tự ưu tiên, tự động thử model tiếp theo nếu gặp lỗi 503/404
    CANDIDATE_MODELS = [
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-3.1-flash-lite-preview",
        "gemini-3.5-flash-lite",
    ]

    try:
        client = genai.Client(api_key=api_key)

        user_content = (
            f"Dưới đây là toàn bộ dữ liệu của khách hàng cần phân tích:\n"
            f"```json\n{json.dumps(context_payload, ensure_ascii=False, indent=2, default=str)}\n```\n"
            f"Hãy phân tích toàn diện theo 4 tiêu chí chuyên sâu và cung cấp tóm tắt tổng quan."
        )

        gen_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=CustomerAnalysisOutput,
            temperature=0.3,
        )

        response = None
        last_error = None
        used_model = None

        for model_id in CANDIDATE_MODELS:
            try:
                logger.info(f"Attempting Gemini model: {model_id}")
                response = client.models.generate_content(
                    model=model_id,
                    contents=user_content,
                    config=gen_config,
                )
                used_model = model_id
                logger.info(f"Success with model: {model_id}")
                break  # Model này hoạt động, dừng vòng lặp
            except Exception as model_err:
                err_str = str(model_err)
                logger.warning(f"Model {model_id} failed: {err_str[:120]}")
                last_error = model_err
                # Nếu lỗi là 503 hoặc 404 thì thử model tiếp theo
                if "503" in err_str or "404" in err_str or "UNAVAILABLE" in err_str or "NOT_FOUND" in err_str:
                    continue
                # Các lỗi khác (400, auth...) thì không thử tiếp
                raise

        if response is None:
            raise last_error  # Hết model để thử

        if not response.text:
            logger.error("Gemini API returned empty response.")
            return _get_fallback_response("Empty response from AI")

        result = json.loads(response.text)

        lead_score = max(1, min(100, int(result.get("lead_score", 50))))

        return {
            "lead_score": lead_score,
            "sentiment": str(result.get("sentiment", "Neutral")),
            "churn_risk": str(result.get("churn_risk", "Medium")),
            "summary": str(result.get("summary", "")),
            "recommended_action": str(result.get("recommended_action", "")),
            "demographics": str(result.get("demographics", "")),
            "rfm_analysis": str(result.get("rfm_analysis", "")),
            "engagement": str(result.get("engagement", "")),
            "predictive": str(result.get("predictive", "")),
        }

    except json.JSONDecodeError as jde:
        logger.error(f"JSON Decode error from Gemini: {jde}")
        return _get_fallback_response(f"JSON decode error: {str(jde)}")
    except Exception as exc:
        logger.error(f"Lỗi khi gọi Google GenAI API: {exc}", exc_info=True)
        return _get_fallback_response(f"AI service error: {str(exc)}")
