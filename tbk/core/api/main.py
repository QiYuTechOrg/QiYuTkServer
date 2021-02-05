from .api import app

__all__ = ["app"]

if __name__ == "__main__":
    import sys

    print("不允许直接运行, 请使用 fastApi/uvicorn 启动", file=sys.stderr)
    sys.exit(1)
