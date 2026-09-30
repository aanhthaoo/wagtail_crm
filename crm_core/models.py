from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Customer(models.Model):
    class StatusChoices(models.TextChoices):
        LEAD = "Lead", "Lead"
        QUALIFIED = "Qualified", "Qualified"
        CUSTOMER = "Customer", "Customer"
        CHURNED = "Churned", "Churned"

    # Thông tin cơ bản khách hàng
    name = models.CharField(max_length=255, verbose_name="Họ và tên")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    company = models.CharField(max_length=255, blank=True, verbose_name="Công ty")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.LEAD,
        verbose_name="Trạng thái khách hàng",
    )

    # Các trường tóm tắt phân tích AI (hiển thị trên bảng)
    ai_lead_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="AI Lead Score (1-100)",
        help_text="Điểm tiềm năng từ 1 đến 100 do AI đánh giá",
    )
    ai_sentiment = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="AI Sentiment",
        help_text="Cảm xúc/thái độ khách hàng (Positive / Neutral / Negative)",
    )
    ai_churn_risk = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="AI Churn Risk",
        help_text="Nguy cơ rời bỏ dịch vụ (Low / Medium / High)",
    )
    ai_summary = models.TextField(
        blank=True,
        verbose_name="AI Summary",
        help_text="Tóm tắt ngắn gọn kết quả phân tích",
    )
    ai_recommended_action = models.TextField(
        blank=True,
        verbose_name="AI Recommended Action",
        help_text="Kết luận và hành động tiếp theo đề xuất bởi AI",
    )

    # === Các trường phân tích AI chuyên sâu (hiển thị trong Modal) ===
    ai_demographics = models.TextField(
        blank=True,
        verbose_name="1. Thuộc tính định danh (Demographics / Firmographics)",
        help_text="Phân tích quy mô công ty, ngành nghề, vị trí địa lý, vai trò người ra quyết định",
    )
    ai_rfm_analysis = models.TextField(
        blank=True,
        verbose_name="2. Hành vi giao dịch (Mô hình RFM)",
        help_text="Recency (thời gian mua gần nhất), Frequency (tần suất), Monetary (giá trị chi tiêu)",
    )
    ai_engagement = models.TextField(
        blank=True,
        verbose_name="3. Mức độ tương tác & Sắc thái (Engagement & Sentiment)",
        help_text="Tần suất phản hồi, số ticket hỗ trợ, phân tích cảm xúc nội dung trao đổi",
    )
    ai_predictive = models.TextField(
        blank=True,
        verbose_name="4. Chỉ số dự đoán & Vòng đời (Predictive Metrics)",
        help_text="Lead Score, vị trí phễu bán hàng, Churn Risk, CLV dự kiến",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    # Wagtail Panels
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("email"),
                FieldPanel("phone"),
                FieldPanel("company"),
                FieldPanel("status"),
            ],
            heading="Thông Tin Khách Hàng",
        ),
        MultiFieldPanel(
            [
                FieldPanel("ai_lead_score"),
                FieldPanel("ai_sentiment"),
                FieldPanel("ai_churn_risk"),
                FieldPanel("ai_summary"),
                FieldPanel("ai_recommended_action"),
            ],
            heading="Tóm Tắt Phân Tích AI",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("ai_demographics"),
                FieldPanel("ai_rfm_analysis"),
                FieldPanel("ai_engagement"),
                FieldPanel("ai_predictive"),
            ],
            heading="Phân Tích AI Chuyên Sâu (4 Tiêu Chí)",
            classname="collapsible collapsed",
        ),
    ]

    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Danh sách Khách hàng"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name


class InteractionHistory(models.Model):
    class ChannelChoices(models.TextChoices):
        EMAIL = "Email", "Email"
        CALL = "Call", "Cuộc gọi"
        MEETING = "Meeting", "Cuộc họp"
        SUPPORT_TICKET = "Support Ticket", "Support Ticket"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="interactions",
        verbose_name="Khách hàng",
    )
    channel = models.CharField(
        max_length=50,
        choices=ChannelChoices.choices,
        default=ChannelChoices.EMAIL,
        verbose_name="Kênh tương tác",
    )
    content = models.TextField(verbose_name="Nội dung tương tác")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tương tác")

    # Wagtail Panels
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("customer"),
                FieldPanel("channel"),
                FieldPanel("content"),
            ],
            heading="Chi Tiết Lịch Sử Tương Tác",
        ),
    ]

    class Meta:
        verbose_name = "Lịch sử tương tác"
        verbose_name_plural = "Lịch sử tương tác"
        ordering = ["-created_at"]

    @admin.display(description="Nội dung tóm tắt")
    def content_preview(self):
        if self.content and len(self.content) > 80:
            return f"{self.content[:80]}..."
        return self.content or ""

    def __str__(self):
        return f"[{self.channel}] {self.customer.name} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class Order(models.Model):
    class StageChoices(models.TextChoices):
        NEGOTIATION = "Negotiation", "Đang đàm phán"
        WON = "Won", "Thành công (Won)"
        LOST = "Lost", "Thất bại (Lost)"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Khách hàng",
    )
    order_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Mã đơn hàng",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Giá trị đơn hàng (VNĐ)",
    )
    stage = models.CharField(
        max_length=20,
        choices=StageChoices.choices,
        default=StageChoices.NEGOTIATION,
        verbose_name="Giai đoạn",
    )
    close_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày dự kiến/thực tế chốt",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    # Wagtail Panels
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("customer"),
                FieldPanel("order_code"),
                FieldPanel("amount"),
                FieldPanel("stage"),
                FieldPanel("close_date"),
            ],
            heading="Thông Tin Đơn Hàng / Cơ Hội",
        ),
    ]

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Danh sách Đơn hàng"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_code} - {self.customer.name} ({self.get_stage_display()})"
