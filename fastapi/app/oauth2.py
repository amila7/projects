from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta


# Secret key to sign the JWT token
#Algorithm used to sign the token
#Expiration time of the token
SECRET_KEY = "e0e4e6f6a7f7c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to create a JWT token

def create_access_token(data: dict):
    to_encode = data.copy()
    # Add the expiration time to the token
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

