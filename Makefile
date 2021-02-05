# 代码生成相关
include mk/code.mk
# 本地开发相关
include mk/local.mk

download-open-api-file:
	rm -f openapi.json || true
	wget https://api.tbk.qiyutech.tech/openapi.json


shell:
	cd tbk && poetry run python manage.py shell

clean-log:
	rm logs/*.log

