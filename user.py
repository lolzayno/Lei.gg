import bcrypt
from sqlalchemy import create_engine, text
import smtplib
import ssl
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import players
import hashlib

def encrypt_pw(password):
    # Use SHA-256 for a consistent hash without salt
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_pw

def check_email(engine, email):
    sql = """
    SELECT * FROM users
    WHERE email = :email
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql),
            {"email": email}
        ).fetchall()

        if result:
            return "Exists"
                                                                                                                                                                                                                                                                                                                                                                                 
def check_username(engine, username):
    sql = """
    SELECT * FROM users
    WHERE username = :username
    """

    with engine.connect() as connection:
        result = connection.execute(text(sql),
            {"username": username}
        ).fetchall()

        if result:
            return "Exists"

def login(engine, username, password):
    encrypted = encrypt_pw(password)
    sql = """
    SELECT * FROM users
    WHERE username = :username
    AND password_encrypt = :password
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {"username": username, "password": encrypted}).fetchall()
        if result:
            return "Success!"
        else:
            return "Incorrect Username or Password"

def create_user(engine, username, email, password):
    insert_sql = """
    INSERT INTO users (username, password_encrypt, email) VALUES (:username, :password, :email)
    """
    
    # Check if the email already exists
    if check_email(engine, email) == "Exists":
        return "Existing User Under Email"
    if check_username(engine, username) == "Exists":
        return "Existing Username"
    encrypted = encrypt_pw(password)
    with engine.connect() as connection:
        # Execute the INSERT statement
        try:
            result = connection.execute(text(insert_sql), {
                "username": username,
                "password": encrypted,
                "email": email
            })
            
            # Commit the transaction
            connection.commit()
            
            return "User Created"
        except Exception as e:
            print("Error inserting user:", e)
            return "Error"


def update_profile_picture(engine, username, image_data):
    sql = """
    UPDATE users
    SET profile_pic = :profile_pic
    WHERE username = :username
    """
    with engine.begin() as connection:  # Using Engine.begin() ensures auto-commit
        result = connection.execute(
            text(sql),
            {"profile_pic": image_data, "username": username}
        )
        if result.rowcount == 0:
            print("No user found with the given username.")
            return "User not found"
    return "Profile picture updated successfully"

def generate_reset_token():
    # Generate a unique, secure token for password reset
    return secrets.token_urlsafe(16)

def send_recovery_email(email, reset_token):
    # Define email sender and receiver
    sender_email = players.get_json("mail")
    receiver_email = email
    password = players.get_json("email")  # Use an app password or email password

    # Create the email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the reset link (In practice, this link would direct to a real reset page on your website)
    reset_link = f"http://yourwebsite.com/reset_password?token={reset_token}"

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi,
    We received a request to reset your password. You can reset it using the following link:
    {reset_link}
    If you didn't request a password reset, please ignore this email.
    """
    html = f"""\
    <html>
      <body>
        <p>Hi,<br>
           We received a request to reset your password. You can reset it using the following link:<br>
           <a href="{reset_link}">Reset your password</a>
           <br><br>
           If you didn't request a password reset, please ignore this email.
        </p>
      </body>
    </html>
    """

    # Attach both plain and HTML versions
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Send the email using SMTP
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def recover(email):
    # Generate a reset token and send the recovery email
    reset_token = generate_reset_token()
    send_recovery_email(email, reset_token)
    print(f"Password recovery email sent to {email}.")

if __name__ == "__main__":
    password = input("Enter a password to encrypt: ")
    encrypted_password = encrypt_pw(password)
    print("Encrypted password:", encrypted_password)
