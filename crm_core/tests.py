import json
import logging
from unittest.mock import MagicMock, patch
from django.test import TestCase, Client
from crm_core.models import Customer, InteractionHistory
from crm_core.services.ai_service import analyze_customer


class CustomerModelTestCase(TestCase):
    """Kiem tra tinh toan ven khi tao ban ghi Customer va InteractionHistory."""

    def setUp(self):
        self.customer = Customer.objects.create(
            name="Pham Minh Duc",
            email="duc.pham@example.com",
            phone="0912345678",
            company="Duc Minh Corp",
            status=Customer.StatusChoices.LEAD,
        )

    def test_customer_creation(self):
        """Kiem tra tao Customer thanh cong voi cac gia tri mac dinh."""
        self.assertEqual(self.customer.name, "Pham Minh Duc")
        self.assertEqual(self.customer.email, "duc.pham@example.com")
        self.assertEqual(self.customer.status, Customer.StatusChoices.LEAD)
        self.assertIsNone(self.customer.ai_lead_score)
        self.assertEqual(str(self.customer), "Pham Minh Duc (Duc Minh Corp)")

    def test_interaction_history_creation(self):
        """Kiem tra tao InteractionHistory lien ket voi Customer."""
        interaction = InteractionHistory.objects.create(
            customer=self.customer,
            channel=InteractionHistory.ChannelChoices.EMAIL,
            content="Khach hang yeu cau tu van goi giai phap doanh nghiep.",
        )
        self.assertEqual(interaction.customer, self.customer)
        self.assertEqual(interaction.channel, InteractionHistory.ChannelChoices.EMAIL)
        self.assertIn("Pham Minh Duc", str(interaction))
        self.assertEqual(self.customer.interactions.count(), 1)


class AIServiceTestCase(TestCase):
    """Kiem thu ai_service.py bang unittest.mock.patch."""

    @patch("crm_core.services.ai_service.genai.Client")
    def test_analyze_customer_success(self, mock_genai_client):
        """Gia lap phan hoi JSON hop le tu Gemini API."""
        mock_ai_response = {
            "lead_score": 88,
            "sentiment": "Positive",
            "churn_risk": "Low",
            "summary": "Khach hang quan tam CRM AI.",
            "recommended_action": "Gui hop dong mau.",
        }

        mock_client_instance = MagicMock()
        mock_model_response = MagicMock()
        mock_model_response.text = json.dumps(mock_ai_response)
        mock_client_instance.models.generate_content.return_value = mock_model_response
        mock_genai_client.return_value = mock_client_instance

        customer_info = {
            "name": "Pham Minh Duc",
            "email": "duc.pham@example.com",
            "status": "Lead",
        }
        interactions = [
            {"channel": "Email", "content": "Khach muon demo."}
        ]

        result = analyze_customer(customer_info, interactions)

        self.assertEqual(result["lead_score"], 88)
        self.assertEqual(result["sentiment"], "Positive")
        self.assertEqual(result["churn_risk"], "Low")
        self.assertEqual(result["summary"], mock_ai_response["summary"])
        self.assertEqual(result["recommended_action"], mock_ai_response["recommended_action"])

    @patch("crm_core.services.ai_service.genai.Client")
    def test_analyze_customer_api_error_fallback(self, mock_genai_client):
        """Kiem tra fallback an toan khi API gap su co."""
        logging.disable(logging.CRITICAL)
        try:
            mock_client_instance = MagicMock()
            mock_client_instance.models.generate_content.side_effect = Exception("API connection timed out")
            mock_genai_client.return_value = mock_client_instance

            result = analyze_customer({"name": "Test User"}, [])

            self.assertEqual(result["lead_score"], 50)
            self.assertEqual(result["sentiment"], "Neutral")
            self.assertEqual(result["churn_risk"], "Medium")
            self.assertIn("error", result)
        finally:
            logging.disable(logging.NOTSET)


class CustomerAIAnalysisEndpointTestCase(TestCase):
    """Kiem tra endpoint /api/customers/<id>/analyze/ tra ve HTTP 200 va ghi dung Database."""

    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            name="Le Thi Thu",
            email="thu.le@abccompany.com",
            phone="0988776655",
            company="ABC Company",
            status=Customer.StatusChoices.QUALIFIED,
        )
        InteractionHistory.objects.create(
            customer=self.customer,
            channel=InteractionHistory.ChannelChoices.CALL,
            content="Trao doi bao gia.",
        )

    @patch("crm_core.views.analyze_customer")
    def test_trigger_customer_ai_analysis_endpoint(self, mock_analyze_customer):
        """Test goi API phan tich AI: tra ve 200 va Customer cap nhat trong DB."""
        mock_analyze_customer.return_value = {
            "lead_score": 90,
            "sentiment": "Positive",
            "churn_risk": "Low",
            "summary": "Khach hang dong y ky hop dong.",
            "recommended_action": "Ky hop dong.",
        }

        url = f"/api/customers/{self.customer.id}/analyze/"
        response = self.client.post(url, content_type="application/json")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["ai_lead_score"], 90)
        self.assertEqual(data["data"]["ai_sentiment"], "Positive")
        self.assertEqual(data["data"]["ai_churn_risk"], "Low")

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.ai_lead_score, 90)
        self.assertEqual(self.customer.ai_sentiment, "Positive")
        self.assertEqual(self.customer.ai_churn_risk, "Low")
        self.assertEqual(self.customer.ai_summary, "Khach hang dong y ky hop dong.")
        self.assertEqual(self.customer.ai_recommended_action, "Ky hop dong.")

    def test_trigger_customer_ai_analysis_not_found(self):
        """Test truong hop customer_id khong ton tai (tra ve 404)."""
        logging.disable(logging.CRITICAL)
        try:
            url = "/api/customers/999999/analyze/"
            response = self.client.post(url, content_type="application/json")
            self.assertEqual(response.status_code, 404)
            data = response.json()
            self.assertFalse(data["success"])
        finally:
            logging.disable(logging.NOTSET)
