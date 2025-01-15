# from access_token import decode_access_token
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDEsInJvbGUiOiJjdXN0b21lciIsImV4cCI6MTczNzEwNjk3N30.S1YsIiekduFKkSXa6fI94jUZQBFIVEXQPf4StUUQg3E"
# print(decode_access_token(token))

from security import hash_password, verify_password

password = "070404"
hashed_password = hash_password(password)
print(hashed_password)

print(verify_password(password, hashed_password))
