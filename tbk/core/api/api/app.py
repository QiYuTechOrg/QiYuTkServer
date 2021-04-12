from ninja import NinjaAPI

__all__ = ["app"]

app = NinjaAPI(
    title="奇遇淘客API",
    description="奇遇淘客内部接口",
    version="v1.0.0",
)


@app.get("/ping", tags=["Ping"], summary="Ping测试", description="测试服务是否正常")
async def ping_view():
    return "pong"
