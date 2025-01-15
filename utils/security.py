import bcrypt

def hash_password(password: str):
    # Tạo salt và băm mật khẩu
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password: str, hashed_password: str):
    # Kiểm tra mật khẩu với giá trị băm đã lưu
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
