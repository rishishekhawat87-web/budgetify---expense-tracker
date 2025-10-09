import sqlite3
from datetime import datetime

class BudgetifyBackend:
    def __init__(self, db_name="budgetify.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                            (id INTEGER PRIMARY KEY, amount REAL, category TEXT, 
                             date TEXT, notes TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS budget
                            (id INTEGER PRIMARY KEY, limit_amount REAL, period TEXT)''')
        self.conn.commit()
    
    def add_expense(self, amount, category, notes=""):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO expenses (amount, category, date, notes) VALUES (?, ?, ?, ?)",
                          (amount, category, date, notes))
        self.conn.commit()
        return "Expense added successfully"
    
    def get_expenses(self, category=None):
        if category:
            self.cursor.execute("SELECT * FROM expenses WHERE category=?", (category,))
        else:
            self.cursor.execute("SELECT * FROM expenses")
        return self.cursor.fetchall()
    
    def set_budget(self, limit_amount, period="monthly"):
        self.cursor.execute("DELETE FROM budget")
        self.cursor.execute("INSERT INTO budget (limit_amount, period) VALUES (?, ?)", 
                          (limit_amount, period))
        self.conn.commit()
        return f"Budget set to ₹{limit_amount} for {period}"
    
    def check_budget_status(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        total = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT limit_amount FROM budget")
        result = self.cursor.fetchone()
        budget = result[0] if result else 0
        return {"total_spent": total, "budget_limit": budget, "remaining": budget - total}
    
    def close(self):
        self.conn.close()
