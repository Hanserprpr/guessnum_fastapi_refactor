from fastapi import FastAPI
from app.database import engine, Base  # 初始化数据库连接
from app.routers import auth  # 导入用户和认证路由模块
from app.config import settings  # 导入配置
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_router import router as user_router
from app.routers.game_router import router as game_router

# 创建 FastAPI 实例
app = FastAPI(
    title="Guess Number Game API",
    description="API for the Guess Number Game application with FastAPI",
    version="1.3.3",
    debug=settings.debug
)

# 数据库初始化
Base.metadata.create_all(bind=engine)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的前端 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册认证路由
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

# 注册游戏路由
app.include_router(game_router, prefix="/api/game", tags=["Game"])

# 根路由
@app.get("/")
def root():
    return {"message": "Welcome to the Guess Number Game API"}

app.include_router(user_router, prefix="/api/user", tags=["User"])
