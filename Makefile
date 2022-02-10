# 代码生成相关
include mk/code.mk
# 本地开发相关
include mk/local.mk
# i18n 命令
include mk/i18n.mk

download-open-api-file:
	rm -f openapi.json || true
	wget https://api.tbk.qiyutech.tech/openapi.json


shell:
	cd tbk && poetry run python manage.py shell

clean-log:
	rm logs/*.log


dev-build:
	docker-compose build --no-cache

dev-run:
	docker-compose up


comby-async-def-dry-run:
	comby -config comby/async_def.toml -directory tbk/core/api/api -matcher .py

comby-async-def-in-place:
	comby -in-place -config comby/async_def.toml -directory tbk/core/api/api -matcher .py

comby-get-ztk-api-v2-dry-run:
	comby -config comby/get_ztk_api_v2.toml -directory tbk -matcher .py

comby-get-ztk-api-v2-in-place:
	comby -in-place -config comby/get_ztk_api_v2.toml -directory tbk -matcher .py


copy-static-to-cdn-git:TARGET_DIR=~/QiYuTechDev/QiYuStatic/tbk
copy-static-to-cdn-git:
	cp -r static/ $(TARGET_DIR)/v3


format:
	poetry run black tbk
