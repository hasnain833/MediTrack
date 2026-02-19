from database.connection import Database
import bcrypt

class BaseModel:
    db = Database()

class User(BaseModel):
    @classmethod
    def find_by_username(cls, username):
        return cls.db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))

    @classmethod
    def find_all(cls):
        return cls.db.fetch_all("SELECT * FROM users ORDER BY role, username")

    @classmethod
    def create(cls, username, password, full_name, role='staff'):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "INSERT INTO users (username, password_hash, full_name, role) VALUES (%s, %s, %s, %s)"
        cls.db.execute_query(query, (username, hashed, full_name, role))

class Medicine(BaseModel):
    @classmethod
    def get_all(cls):
        return cls.db.fetch_all("SELECT * FROM inventory ORDER BY medicine_name")

    @classmethod
    def search(cls, term):
        query = "SELECT * FROM inventory WHERE medicine_name LIKE %s OR category LIKE %s"
        pattern = f"%{term}%"
        return cls.db.fetch_all(query, (pattern, pattern))

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO inventory (medicine_name, category, company, batch_no, expiry_date, stock_qty, price, reorder_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('medicine_name'),
            data.get('category'),
            data.get('company'),
            data.get('batch_no'),
            data.get('expiry_date'),
            data.get('stock_qty', 0),
            data.get('price', 0.0),
            data.get('reorder_level', 10)
        )
        cls.db.execute_query(query, params)

    @classmethod
    def get_low_stock_count(cls):
        res = cls.db.fetch_one("SELECT COUNT(*) as count FROM inventory WHERE stock_qty <= reorder_level")
        return res['count'] if res else 0

    @classmethod
    def update_stock(cls, med_id, qty_change):
        query = "UPDATE inventory SET stock_qty = stock_qty + %s WHERE id = %s"
        cls.db.execute_query(query, (qty_change, med_id))

class Customer(BaseModel):
    @classmethod
    def find_or_create(cls, name, phone=None):
        if phone:
            existing = cls.db.fetch_one("SELECT * FROM customers WHERE phone = %s", (phone,))
            if existing: return existing
        
        query = "INSERT INTO customers (name, phone) VALUES (%s, %s)"
        cursor = cls.db.execute_query(query, (name, phone))
        cust_id = cursor.lastrowid
        cursor.close()
        return cls.db.fetch_one("SELECT * FROM customers WHERE id = %s", (cust_id,))

class Sale(BaseModel):
    @classmethod
    def create_transaction(cls, bill_no, user_id, customer_id, items, totals):
        # totals: (total_amount, tax_amount, grand_total)
        sale_query = """
            INSERT INTO sales (bill_no, customer_id, user_id, total_amount, tax_amount, grand_total)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = cls.db.execute_query(sale_query, (bill_no, customer_id, user_id, *totals))
        sale_id = cursor.lastrowid
        cursor.close()

        item_query = """
            INSERT INTO sale_items (sale_id, inventory_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        for item in items:
            # item: (inventory_id, quantity, unit_price, subtotal)
            cls.db.execute_query(item_query, (sale_id, *item))
            # Also update inventory stock
            Medicine.update_stock(item[0], -item[1])
        
        return sale_id

    @classmethod
    def get_todays_stats(cls):
        query = """
            SELECT COUNT(*) as count, SUM(grand_total) as revenue 
            FROM sales 
            WHERE DATE(created_at) = CURDATE()
        """
        res = cls.db.fetch_one(query)
        return {
            'revenue': float(res['revenue'] or 0),
            'orders': res['count'] or 0
        }

class AuditLog(BaseModel):
    @classmethod
    def log(cls, user_id, action, module, description, ip="127.0.0.1"):
        query = """
            INSERT INTO audit_logs (user_id, action_type, module_name, description, ip_address)
            VALUES (%s, %s, %s, %s, %s)
        """
        cls.db.execute_query(query, (user_id, action, module, description, ip))