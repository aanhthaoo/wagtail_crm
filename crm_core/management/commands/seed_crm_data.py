import datetime
from django.core.management.base import BaseCommand
from crm_core.models import Customer, InteractionHistory, Order


class Command(BaseCommand):
    help = "Seed mock data for Customers, Interaction History, and Orders (AI fields left blank for real analysis)"

    def handle(self, *args, **options):
        # Lưu ý: Các trường AI (ai_lead_score, ai_sentiment, ai_churn_risk, v.v.)
        # được để TRỐNG có chủ đích. Dữ liệu AI thật sẽ được tạo khi bấm nút
        # "Phân tích AI" trên Dashboard để gọi Gemini API.
        customers_data = [
            {
                "name": "Nguyen Hoang Nam",
                "email": "nam.nguyen@vinacorp.vn",
                "phone": "0987654321",
                "company": "VinaCorp Solutions",
                "status": Customer.StatusChoices.QUALIFIED,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Khach hang lien he trao doi ve bai toan chuyen doi so va tu dong hoa quy trinh cham soc khach hang 24/7 bang AI.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Hop truc tiep cung CTO & Truong phong Kinh doanh tai tru so, demo he thong Wagtail AI CRM va tinh nang Lead Scoring.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Gui bao gia chi tiet goi Enterprise 150 trieu dong kem cam ket SLA uptime 99.9% va bao mat du lieu.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Nam phan hoi rat hai long voi ban de xuat, dang trinh Ban Giam doc phe duyet ngan sach quy 4.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-001",
                        "amount": 150000000.00,
                        "stage": Order.StageChoices.NEGOTIATION,
                        "close_date": datetime.date(2026, 10, 15),
                    }
                ],
            },
            {
                "name": "Tran Thi Mai Anh",
                "email": "maianh.tran@techviet.io",
                "phone": "0912345678",
                "company": "TechViet Media",
                "status": Customer.StatusChoices.CUSTOMER,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Dang ky tu van goi phan mem Core CRM cho 20 nhan su phong Marketing va Sales.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Ky ket hop dong trien khai giai doan 1 tri gia 85 trieu dong thanh cong.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.SUPPORT_TICKET,
                        "content": "Yeu cau ho tro cau hinh webhook ket noi voi nen tang email marketing tu dong. Da xu ly xong trong 2h.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "CSKH dinh ky quy 3: Khach hang danh gia 10/10 ve tinh tien dung va toc do xu ly ho tro.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Ban thao mo rong them 50 tai khoan user va tich hop module AI phan tich hanh vi nguoi dung.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-002",
                        "amount": 85000000.00,
                        "stage": Order.StageChoices.WON,
                        "close_date": datetime.date(2026, 8, 20),
                    },
                    {
                        "order_code": "ORD-2026-003",
                        "amount": 120000000.00,
                        "stage": Order.StageChoices.NEGOTIATION,
                        "close_date": datetime.date(2026, 11, 1),
                    },
                    {
                        "order_code": "ORD-2026-007",
                        "amount": 45000000.00,
                        "stage": Order.StageChoices.WON,
                        "close_date": datetime.date(2026, 1, 15),
                    },
                ],
            },
            {
                "name": "Le Van Tuan",
                "email": "tuan.le@globaltrade.com",
                "phone": "0908112233",
                "company": "Global Trade Logistics",
                "status": Customer.StatusChoices.CUSTOMER,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Ky hop dong trien khai phan mem quan ly van don va cham soc khach hang nganh logistics.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.SUPPORT_TICKET,
                        "content": "Bao loi dong bo du lieu ton kho giua chi nhanh Hai Phong va TP.HCM, thoi gian xu ly cham mat 48h.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Khach hang bay to su that vong sau su co nghen mang gio cao diem, yeu cau boi thuong dich vu.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.SUPPORT_TICKET,
                        "content": "Khieu nai bao cao doanh thu quy 2 bi sai lech so lieu giua cac kenh thanh toan.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Giam doc CSKH gui email thu loi kem de xuat giam 20% phi gia han nam toi nhung khach chua hoi am.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-004",
                        "amount": 65000000.00,
                        "stage": Order.StageChoices.WON,
                        "close_date": datetime.date(2026, 5, 10),
                    },
                    {
                        "order_code": "ORD-2026-008",
                        "amount": 90000000.00,
                        "stage": Order.StageChoices.LOST,
                        "close_date": datetime.date(2026, 9, 15),
                    },
                ],
            },
            {
                "name": "Pham Quang Huy",
                "email": "huy.pham@greenenergy.vn",
                "phone": "0934567890",
                "company": "Green Energy Vietnam",
                "status": Customer.StatusChoices.LEAD,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Gui yeu cau bao gia he thong quan ly doi tac dien mat troi qua form website.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Sales lien he xac nhan: quy mo cong ty 35 nhan su, can trien khai giai phap trong thang 11/2026.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Demo online qua Google Meet, huong dan su dung tinh nang phan loai Lead va pipeline quan ly co hoi.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Gui de xuat ky thuat va bang phan tich so sanh chi phi voi cac doi thu tren thi truong.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-005",
                        "amount": 95000000.00,
                        "stage": Order.StageChoices.NEGOTIATION,
                        "close_date": datetime.date(2026, 10, 30),
                    }
                ],
            },
            {
                "name": "Do Thi Bich Hanh",
                "email": "hanh.do@fastretail.vn",
                "phone": "0977889900",
                "company": "Fast Retail Chain",
                "status": Customer.StatusChoices.CHURNED,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Khao sat nhu cau he thong CRM cho chuoi 12 cua hang ban le tien loi.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Hop trinh bay giai phap ket noi may POS ban hang va chuong trinh tich diem khach hang than thiet.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Khach hang thong bao ngung du an vi suy giam doanh thu ban le va cat giam ngan sach cong nghe.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Xac nhan huy deal va dong tai khoan thu nghiem, khach chuyen sang dung file Excel quan ly.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-006",
                        "amount": 40000000.00,
                        "stage": Order.StageChoices.LOST,
                        "close_date": datetime.date(2026, 7, 1),
                    }
                ],
            },
            {
                "name": "Vo Minh Tri",
                "email": "tri.vo@nextgenfin.io",
                "phone": "0945112288",
                "company": "NextGen FinTech JSC",
                "status": Customer.StatusChoices.QUALIFIED,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Tiep can qua su kien Trien lam Cong nghe Tai chinh FinTech Summit 2026.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Hop danh gia ky thuat voi doi ngu Bao mat & Compliance, yeu cau chuan ma hoa du lieu cao cap.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.SUPPORT_TICKET,
                        "content": "Ho tro cap sandbox API de doi tech ben khach test ket noi danh gia hieu nang.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Giam doc Van hanh (COO) khen ngoi API chuan RESTful rat de tich hop, hen chot hop dong vao cuoi thang.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-009",
                        "amount": 250000000.00,
                        "stage": Order.StageChoices.NEGOTIATION,
                        "close_date": datetime.date(2026, 10, 25),
                    }
                ],
            },
            {
                "name": "Dang Thu Thao",
                "email": "thao.dang@edusmart.edu.vn",
                "phone": "0968991122",
                "company": "EduSmart Online Academy",
                "status": Customer.StatusChoices.CUSTOMER,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Tu van phan mem quan ly thong tin 5000 hoc vien va he thong gui thong bao tu dong.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Ky hop dong goi Starter tri gia 35 trieu dong thanh cong.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.SUPPORT_TICKET,
                        "content": "Yeu cau tich hop cong thanh toan hoc phi tu dong qua MoMo va VNPay, da hoan tat sau 24h.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Khach gui thu khen ngoi doi ngu support nhiet tinh, dang ky nang cap len goi Pro toan dien.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.MEETING,
                        "content": "Hop ky ket hop dong mo rong cho 4 chi nhanh moi mo tai Ha Noi va Da Nang.",
                    },
                ],
                "orders": [
                    {
                        "order_code": "ORD-2026-010",
                        "amount": 35000000.00,
                        "stage": Order.StageChoices.WON,
                        "close_date": datetime.date(2026, 2, 15),
                    },
                    {
                        "order_code": "ORD-2026-011",
                        "amount": 75000000.00,
                        "stage": Order.StageChoices.WON,
                        "close_date": datetime.date(2026, 8, 10),
                    },
                    {
                        "order_code": "ORD-2026-012",
                        "amount": 50000000.00,
                        "stage": Order.StageChoices.NEGOTIATION,
                        "close_date": datetime.date(2026, 11, 20),
                    },
                ],
            },
            {
                "name": "Hoang Quoc Bao",
                "email": "bao.hoang@baoanlogistics.vn",
                "phone": "0909556677",
                "company": "Bao An Supply Chain",
                "status": Customer.StatusChoices.LEAD,
                "interactions": [
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Dang ky tai tai lieu Huong dan toi uu chuoi cung ung bang AI tren website.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.CALL,
                        "content": "Nhan vien sales goi dien tu van nhung khach ban hen goi lai vao dip khac.",
                    },
                    {
                        "channel": InteractionHistory.ChannelChoices.EMAIL,
                        "content": "Gui email follow-up va moi tham gia hoi thao truc tuyen, khach chua mo email.",
                    },
                ],
                "orders": [],
            },
        ]

        created_cust_count = 0
        created_int_count = 0
        created_ord_count = 0

        for data in customers_data:
            interactions = data.pop("interactions", [])
            orders = data.pop("orders", [])

            customer, created = Customer.objects.update_or_create(
                email=data["email"],
                defaults=data,
            )
            if created:
                created_cust_count += 1

            for item in interactions:
                _, int_created = InteractionHistory.objects.get_or_create(
                    customer=customer,
                    channel=item["channel"],
                    content=item["content"],
                )
                if int_created:
                    created_int_count += 1

            for ord_item in orders:
                _, ord_created = Order.objects.update_or_create(
                    order_code=ord_item["order_code"],
                    defaults={
                        "customer": customer,
                        "amount": ord_item["amount"],
                        "stage": ord_item["stage"],
                        "close_date": ord_item["close_date"],
                    },
                )
                if ord_created:
                    created_ord_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported mock CRM data!\n"
                f"- Customers: {len(customers_data)} (AI fields are BLANK - use 'Phan tich AI' button on Dashboard)\n"
                f"- Interactions: {created_int_count}\n"
                f"- Orders: {created_ord_count}"
            )
        )
