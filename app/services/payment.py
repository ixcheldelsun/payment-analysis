import datetime 

class PaymentService:
    
    def __init__(self):
        self.name = "Payment Service."
    
    def get_all_payments(self, cur):
        cur.execute("SELECT user, amount, DATE_FORMAT(date_created, '%d %m %Y')  FROM payments;")
        payments = cur.fetchall()
        return str(payments), 200

    
    def create_payment(self, cur, db, user_id:int, data:dict):
        try:
            cur.execute(
                f"""INSERT INTO payments VALUES (NULL, %s, %s, %s)""", 
                (user_id, data["amount"], datetime.datetime.utcnow(),)
            )
            db.connection.commit()
            return "payment created successfully", 201
        except Exception as e:
            print(str(e))
            return str(e), 500
        
        
    def get_user_payments_summary(self, cur, user_id:int):
        data = {}
        try:
            cur.execute(f"""
                SELECT MONTHNAME(date_created), COUNT(id) FROM payments
                WHERE user = {user_id}                               
                GROUP BY MONTHNAME(date_created) 
            """)
            data["monthly_payments"] = dict(cur.fetchall())
            cur.execute(f"""
                SELECT SUM(cast(amount AS DECIMAL(10,2))) as value
                FROM payments
                WHERE user = {user_id}                               
            """)
            data["total_balance"] = cur.fetchone()[0]
            cur.execute(f"""
                SELECT t.type, ROUND(AVG(t.value), 2)
                FROM (
                    SELECT cast(amount AS DECIMAL(10,2)) as value, 
                    CASE
                        WHEN cast(amount AS DECIMAL(10,2)) > 0 THEN 'credit' ELSE 'debit'
                    END AS 'type'
                    FROM payments
                    WHERE user = {user_id}
                ) AS t
                GROUP BY t.type            
            """)
            data["avg_by_type"] = dict(cur.fetchall())
        except Exception as e:
            print(str(e))
            return "An error occurred while getting user payments summary.", 500
        return data
    

service = PaymentService()
