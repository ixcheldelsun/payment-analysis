
def check_credentials(cur, email:str):
    cur.execute('SELECT * FROM users WHERE email = % s', (email, ))
    return bool(cur.fetchone())