# 生成代码相关的命令

# 这是 code 控制器生成的代码目录
code_src_dir:=~/QiYuTechDev/code
# 运行 code
code_run:=cd $(code_src_dir) && poetry run python code


gen-resp-from-json:
	poetry run python code_gen/json_code_gen_resp.py  api/ztk/

gen-model-from-json:
	poetry run python code_gen/json_code_gen_model.py api/ztk/

# 使用 open api 生成 kotlin 数据模型
gen-kotlin-dt-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-kotlin-dt-from-open-api:prefix-file=$(shell pwd)/code_gen/kotlin/dt/prefix.txt
gen-kotlin-dt-from-open-api:postfix-file=$(shell pwd)/code_gen/kotlin/dt/postfix.txt
gen-kotlin-dt-from-open-api:output=$(shell pwd)/../android/app/src/main/java/com/qiyutech/tbk/dt/DtsV2.kt
gen-kotlin-dt-from-open-api:
	$(code_run) kotlin dt   --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)

# 使用 open api 生成 kotlin 代码 stub
gen-kotlin-stub-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-kotlin-stub-from-open-api:prefix-file=$(shell pwd)/code_gen/kotlin/stub/prefix.txt
gen-kotlin-stub-from-open-api:postfix-file=$(shell pwd)/code_gen/kotlin/stub/postfix.txt
gen-kotlin-stub-from-open-api:output=$(shell pwd)/../android/app/src/main/java/com/qiyutech/tbk/dt/Stub.kt
gen-kotlin-stub-from-open-api:export TBK_API_NAME=TbkAPIUrls
gen-kotlin-stub-from-open-api:
	$(code_run) kotlin stub --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)


gen-kotlin-path-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-kotlin-path-from-open-api:prefix-file=$(shell pwd)/code_gen/kotlin/path/prefix.txt
gen-kotlin-path-from-open-api:postfix-file=$(shell pwd)/code_gen/kotlin/path/postfix.txt
gen-kotlin-path-from-open-api:output=$(shell pwd)/../android/app/src/main/java/com/qiyutech/tbk/values/ApiUrlsV2.kt
gen-kotlin-path-from-open-api:
	$(code_run) kotlin path --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)


gen-kotlin-all-from-open-api: gen-kotlin-dt-from-open-api gen-kotlin-path-from-open-api gen-kotlin-stub-from-open-api


gen-swift-path-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-swift-path-from-open-api:prefix-file=$(shell pwd)/code_gen/swift/path/prefix.txt
gen-swift-path-from-open-api:postfix-file=$(shell pwd)/code_gen/swift/path/postfix.txt
gen-swift-path-from-open-api:output=$(shell pwd)/../iOS/tbk/MyGenV2Urls.swift
gen-swift-path-from-open-api:
	$(code_run) swift path --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)


gen-swift-stub-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-swift-stub-from-open-api:prefix-file=$(shell pwd)/code_gen/swift/stub/prefix.txt
gen-swift-stub-from-open-api:postfix-file=$(shell pwd)/code_gen/swift/stub/postfix.txt
gen-swift-stub-from-open-api:output=$(shell pwd)/../iOS/tbk/MyGenV2Slots.swift
gen-swift-stub-from-open-api:
	$(code_run) swift stub --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)

gen-swift-dt-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-swift-dt-from-open-api:prefix-file=$(shell pwd)/code_gen/swift/dt/prefix.txt
gen-swift-dt-from-open-api:postfix-file=$(shell pwd)/code_gen/swift/dt/postfix.txt
gen-swift-dt-from-open-api:output=$(shell pwd)/../iOS/tbk/MyGenV2Types.swift
gen-swift-dt-from-open-api:
	$(code_run) swift dt --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)


gen-swift-all-from-open-api: gen-swift-path-from-open-api gen-swift-dt-from-open-api gen-swift-stub-from-open-api

gen-ts-path-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-ts-path-from-open-api:prefix-file=$(shell pwd)/code_gen/ts/path/prefix.txt
gen-ts-path-from-open-api:postfix-file=$(shell pwd)/code_gen/ts/path/postfix.txt
gen-ts-path-from-open-api:output=$(shell pwd)/../html/ts/api_urls.ts
gen-ts-path-from-open-api:
	@echo "生成 ts path 代码"
	$(code_run) ts path --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)

gen-ts-dt-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-ts-dt-from-open-api:prefix-file=$(shell pwd)/code_gen/ts/dt/prefix.txt
gen-ts-dt-from-open-api:postfix-file=$(shell pwd)/code_gen/ts/dt/postfix.txt
gen-ts-dt-from-open-api:output=$(shell pwd)/../html/ts/api_dts.ts
gen-ts-dt-from-open-api:
	@echo "生成 ts dt 代码"
	$(code_run) ts dt   --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)

gen-ts-stub-from-open-api:openapi-file=$(shell pwd)/openapi.json
gen-ts-stub-from-open-api:prefix-file=$(shell pwd)/code_gen/ts/stub/prefix.txt
gen-ts-stub-from-open-api:postfix-file=$(shell pwd)/code_gen/ts/stub/postfix.txt
gen-ts-stub-from-open-api:output=$(shell pwd)/../html/ts/api_stubs.ts
gen-ts-stub-from-open-api:
	@echo "生成 ts stub 代码"
	$(code_run) ts stub --prefix $(prefix-file) --postfix $(postfix-file) --output $(output) $(openapi-file)

gen-ts-all-from-open-api: gen-ts-path-from-open-api gen-ts-dt-from-open-api gen-ts-stub-from-open-api
	# 生成所有的 ts 相关的代码
