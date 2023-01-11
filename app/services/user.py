
class UserService:
    def __init__(self):
        self.name = "User Service."
        
    def check_user_credentials(self, cur, email:str):
        cur.execute('SELECT * FROM users WHERE email = % s', (email, ))
        return bool(cur.fetchone())


    def create_user(self, cur, db, email:str, password:str):
        exists = self.check_user_credentials(cur, email)
        if not exists:
            cur.execute(
                f"INSERT INTO users VALUES (NULL, % s, % s);", (email, password)
            )
            db.connection.commit()
            return "user created successfully", 201
        else:
            return "email already used", 400
    

    def get_all_users(self, cur):
        cur.execute("SELECT email FROM users;")
        users = cur.fetchall()
        return str(users), 200
    
    
    def get_user(self, cur, email:str):
        try:
            cur.execute('SELECT id FROM users WHERE email = % s', (email, ))
            return cur.fetchone()[0]
        except TypeError:
            return None


service = UserService()