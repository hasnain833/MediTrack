import json
import os

class TemplateService:
    DEFAULT_TEMPLATE = {
        "store": {
            "name": "D. CHEMIST",
            "tagline": "Your Health, Our Priority",
            "address": "123 Pharmacy St, District Karachi\nSindh, Pakistan - 74000\n+92-321-1234567 | care@dchemist.com",
            "color": "#0F172A",
            "tagline_color": "#64748B",
            "address_color": "#64748B"
        },
        "theme": {
            "primary": "#2C7878",
            "accent": "#0F172A",
            "background": "#FFFFFF",
            "text": "#0F172A",
            "font_family": "Inter"
        },
        "table": {
            "header_bg": "rgba(44, 120, 120, 0.08)",
            "header_text": "#2C7878",
            "row_border": "#F1F5F9",
            "columns": ["ITEM", "BATCH", "EXPIRY", "QTY", "RATE", "GST%", "AMOUNT"]
        },
        "footer": {
            "show_qr": True,
            "show_bank": True,
            "thanks_text": "Thank you for your visit!",
            "thanks_color": "#2C7878"
        }
    }

    FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "bill_template.json")

    @classmethod
    def load_template(cls):
        if not os.path.exists(cls.FILE_PATH):
            os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
            cls.save_template(cls.DEFAULT_TEMPLATE)
            return cls.DEFAULT_TEMPLATE
        
        try:
            with open(cls.FILE_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading template: {e}")
            return cls.DEFAULT_TEMPLATE

    @classmethod
    def save_template(cls, template_data):
        try:
            os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
            with open(cls.FILE_PATH, 'w') as f:
                json.dump(template_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

    @classmethod
    def reset_template(cls):
        return cls.save_template(cls.DEFAULT_TEMPLATE)
