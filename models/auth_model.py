from config import connection as c

def get_user_auth(username: str, password: str) -> int:
    with c.cursor() as cursor:
        sql = "SELECT `id`, `username`, `password` FROM `user` WHERE `username`=%s AND `password`=%s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()
        if result is None:
            raise Exception("Incorrect username or password.")
        return result