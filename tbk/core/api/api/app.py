import time

from fastapi import FastAPI, Request
from fastapi.exceptions import ValidationError
from fastapi.middleware.cors import CORSMiddleware

from core.logger import get_error_logger, get_time_logger

__all__ = ["app"]

app = FastAPI(
    title="奇遇淘客API",
    description="奇遇淘客内部接口",
    debug=False,
    version="v1.0.0",
    on_startup=[],
    on_shutdown=[],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

time_logger = get_time_logger()


@app.middleware("http")
async def add_time_log(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    time_logger.bind(consume=process_time, url=str(request.url)).info("time")
    return response


error_logger = get_error_logger()


@app.exception_handler(ValidationError)
async def my_validation_error_handler(request, exc):
    error_logger.bind(exc=exc, request=request).error("validation error")


@app.get("/ping", tags=["Ping"], summary="Ping测试", description="测试服务是否正常")
async def ping_view():
    return "pong"
