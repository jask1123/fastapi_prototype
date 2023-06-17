from fastapi import FastAPI, Security, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from user import Auth, SignInRequestModel, SignUpRequestModel, UserAuthResponseModel, \
    UserResponseModel, UserUpdateRequestModel, get_all_users, get_user_by_id, register_user, \
    signin_user, update_user

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:4000",
    "http://localhost:19006"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
auth_handler = Auth()


###############################
########## Auth APIs ##########
###############################

@app.post('/v1/signup', response_model=UserAuthResponseModel)
def signup_api(user_details: SignUpRequestModel):
    """
    This sign-up API allow you to register your account, and return access token.
    """
    user = register_user(user_details)
    access_token = auth_handler.encode_token(user_details.email)
    refresh_token = auth_handler.encode_refresh_token(user_details.email)
    return JSONResponse(status_code=200, content={
        'token': {'access_token': access_token, 'refresh_token': refresh_token}, 'user': user})


@app.post('/v1/signin', response_model=UserAuthResponseModel)
def signin_api(user_details: SignInRequestModel):
    """
    This sign-in API allow you to obtain your access token.
    """
    user = signin_user(user_details.email, user_details.password)
    access_token = auth_handler.encode_token(user['email'])
    refresh_token = auth_handler.encode_refresh_token(user['email'])
    return JSONResponse(status_code=200, content={
        'token': {'access_token': access_token, 'refresh_token': refresh_token}, 'user': user})


@app.get('/v1/refresh-token')
def refresh_token_api(refresh_token: str):
    """
    This refresh-token API allow you to obtain new access token.
    """
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}


################################
########## Users APIs ##########
################################

@app.get("/v1/users", response_model=list[UserResponseModel])
def get_all_users_api(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    This users get API allow you to fetch all user data.
    """
    token = credentials.credentials
    if (auth_handler.decode_token(token)):
        user = get_all_users()
        return JSONResponse(status_code=200, content=jsonable_encoder(user))
    return JSONResponse(status_code=401, content={'error': 'Faild to authorize'})


@app.get("/v1/user/{user_id}", response_model=UserResponseModel)
def get_user_api(user_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    This user API allow you to fetch specific user data.
    """
    token = credentials.credentials
    if (auth_handler.decode_token(token)):
        user = get_user_by_id(user_id)
        return JSONResponse(status_code=200, content=jsonable_encoder(user))
    return JSONResponse(status_code=401, content={'error': 'Faild to authorize'})


@app.post("/v1/user/update", response_model=UserResponseModel)
def update_user_api(user_details: UserUpdateRequestModel,
                    credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    This user update API allow you to update user data.
    """
    token = credentials.credentials
    if (auth_handler.decode_token(token)):
        user = update_user(user_details)
        return JSONResponse(status_code=200, content=jsonable_encoder(user))
    return JSONResponse(status_code=401, content={'error': 'Faild to authorize'})


###############################
########## Test APIs ##########
###############################

@app.get('/secret')
def secret_data_api(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    This secret API is just for testing. Need access token to access this API.
    """
    token = credentials.credentials
    if (auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'


@app.get('/not-secret')
def not_secret_data_api():
    """
    This not-secret API is just for testing.
    """
    return 'Not secret data'


###############################
########## websocket APIs ##########
###############################

clients = {}

# WebSocket接続用のエンドポイント
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    try:
        while True:
            # クライアントからメッセージを受信
            data = await ws.receive_text()
            # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
            for client in list(clients.values()):
                try:
                    await client.send_text(f"ID: {key} | Message: {data}")
                except:
                    # 接続が切れた場合、当該クライアントを削除する
                    del clients[client]
    except:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]
