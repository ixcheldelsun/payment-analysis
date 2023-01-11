
def check_credentials(cur, email:str):
    cur.execute('SELECT * FROM users WHERE email = % s', (email, ))
    return bool(cur.fetchone())


def get_user(cur, email:str):
    cur.execute('SELECT id FROM users WHERE email = % s', (email, ))
    return cur.fetchone()[0]


def get_payments_summary(cur, email:str):
    user = get_user(cur, email)
    data = {}
    cur.execute(f"""
        SELECT MONTHNAME(date_created), COUNT(id) FROM payments
        WHERE user = {user}                               
        GROUP BY MONTHNAME(date_created) 
    """)
    data["monthly_payments"] = dict(cur.fetchall())
    cur.execute(f"""
        SELECT SUM(cast(amount AS DECIMAL(10,2))) as value
        FROM payments
        WHERE user = {user}                               
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
            WHERE user = {user}
        ) AS t
        GROUP BY t.type            
    """)
    data["avg_by_type"] = dict(cur.fetchall())
    return data