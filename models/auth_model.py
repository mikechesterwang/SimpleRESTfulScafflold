from config import connection as c
from config import verification_code_email as email_config
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import hashlib

def get_user_auth(username: str, password: str) -> int:
    password = hashlib.sha256(password.encode()).hexdigest()
    with c().cursor() as cursor:
        sql = "SELECT `id`, `username`, `password` FROM `user` WHERE `username`=%s AND `password`=%s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()
        if result is None:
            raise Exception("Incorrect username or password.")
        return result


def _generate_code():
    tmp = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    code = "X-"
    for i in range(6):
        code += tmp[random.randint(0, len(tmp) - 1)]
    return code


def _send_email(receiver_email: str, code: str):
    message = MIMEText(email_config['content'].format(code), email_config['content-type'], "utf-8")
    message['Subject'] = email_config['subject']
    message['To'] = receiver_email
    message['From'] = str(Header(email_config['from']))

    mailbox = smtplib.SMTP_SSL(email_config['host'], email_config['port'])
    mailbox.login(email_config['email'], email_config['password'])
    mailbox.sendmail(email_config['email'], receiver_email, message.as_string())


def change_password(username: str, old_password: str, new_password: str, email: str, code: str):
    connection = c()
    new_password = hashlib.sha256(new_password.encode()).hexdigest()
    old_password = hashlib.sha256(old_password.encode()).hexdigest()
    with connection.cursor() as cursor:
        # check if the email and usernamae are matched
        sql = "SELECT COUNT(*) AS cnt FROM user WHERE `email`=%s AND `username`=%s"
        cursor.execute(sql, (email, username))
        result = cursor.fetchone()
        if result['cnt'] == 0:
            raise Exception("The username and email are not matched.")
        
        # check if the code is valid
        sql = "SELECT `created_time` FROM verification_code WHERE `email`=%s AND `code`=%s"
        cursor.execute(sql, (email, code))
        result = cursor.fetchone()

        if result is None:
            raise Exception("Code is expired.")
        
        created_time = result['created_time']
        
        if datetime.now() > created_time + timedelta(minutes=3):
            raise Exception("Code is expired.")

        # the code is valid
        sql = "SELECT COUNT(*) AS cnt FROM `user` WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, old_password))
        result = cursor.fetchone()

        if result['cnt'] == 0:
            raise Exception("Incorrect username or password.")
        
        # code and password are all valid
        sql = "UPDATE `user` SET password=%s WHERE username=%s"
        cursor.execute(sql, (new_password, username))
        connection.commit()


def register(username: str, password: str, email: str, code: str):
    connection = c()
    password = hashlib.sha256(password.encode()).hexdigest()
    with connection.cursor() as cursor:
        # check whether the username or password exists.
        sql = "SELECT COUNT(*) AS cnt FROM `user` WHERE `username`=%s OR `password`=%s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()
        if result['cnt'] != 0:
            raise Exception("Username or email already exists.")

        # check if the code is valie or not
        sql = "SELECT `created_time` FROM verification_code WHERE `email`=%s AND `code`=%s"
        cursor.execute(sql, (email, code))
        result = cursor.fetchone()

        if result is None:
            raise Exception("Code is expired.")
        
        created_time = result['created_time']
        
        if datetime.now() > created_time + timedelta(minutes=3):
            raise Exception("Code is expired.")

        sql = "INSERT INTO `user` (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, email))
        connection.commit()


def get_code(email: str):
    connection = c()
    with connection.cursor() as cursor:
        sql = "SELECT `email`, `code`, `created_time` FROM `verification_code` WHERE `email`=%s"
        cursor.execute(sql, (email))
        result = cursor.fetchone()

        if result is None: # Create new one for it.
            sql = "INSERT INTO `verification_code` (email, code, created_time) VALUES (%s, %s, %s)"
            code = _generate_code()
            cursor.execute(sql, (email, _generate_code(), datetime.now()))
            connection.commit()
        else: # there is a code exists.
            created_time = result['created_time']
            code = result['code']
            email = result['email']
            
            now = datetime.now()

            if now < created_time + timedelta(minutes=1): # within one miniute
                raise Exception("Too frequent access. Wait for one minute and try again.")

            if now > created_time + timedelta(minutes=2): # regenerate code
                sql = "UPDATE `verification_code` SET code=%s, created_time=%s where email=%s"
                cursor.execute(sql, (_generate_code(), datetime.now(), email))
                connection.commit()
        
        # send email
        _send_email(email, code)
            

def verify_code(email: str, code: str):
    with c().cursor() as cursor:
        sql = "SELECT `created_time` FROM verification_code WHERE `email`=%s AND `code`=%s"
        cursor.execute(sql, (email))
        result = cursor.fetchone()

        if result is None:
            return False
        
        created_time = result['created_time']
        
        if datetime.now() > created_time + timedelta(minutes=3):
            return False

        return True