
def check_credentials(cur, email:str):
    cur.execute('SELECT * FROM users WHERE email = % s', (email, ))
    return bool(cur.fetchone())


def get_user(cur, email:str):
    cur.execute('SELECT id FROM users WHERE email = % s', (email, ))
    return cur.fetchone()[0]