# 奇遇淘客 APP 服务器端

## 奇遇淘客代码库

* [奇遇淘客 iOS APP](https://github.com/QiYuTechDev/QiYuTkiOS)
* [奇遇淘客 Android APP](https://github.com/QiYuTechDev/QiYuTkAndroid)

## 奇遇淘客文档

[文档](https://tbk.qiyutech.tech/)

## 博客文章

[奇遇淘客系统已开源](https://blog.qiyutech.tech/202102/05_tbk_server/)

## 技术堆栈

* Python
* Django
* FastAPI

## docker 标签

[Docker Tags](https://hub.docker.com/r/qiyutech/tbk/tags)

所有的 TAG 都是一致的，通过 Github Action 自动推送

```shell
# 如果您需要使用 docker 官方镜像，请使用
docker pull qiyutech/tbk:${TAG}

# 如果您需要使用 ghcr 镜像, 请使用
docker pull ghcr.io/qiyutechdev/tbk:${TAG}

# 中国的用户可能需要使用 阿里云 镜像
# 下载速度比较快
# 如果您需要使用 阿里云 镜像, 请使用
docker pull registry.cn-hangzhou.aliyuncs.com/qiyutech/tbk:${TAG}
```
