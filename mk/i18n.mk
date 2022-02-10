djangoRun:=cd tbk && poetry run python manage.py

# i18n 提取出翻译的字符串
i18n-extract:
	$(djangoRun) makemessages --locale en
	$(djangoRun) makemessages --locale zh_Hans
	$(djangoRun) makemessages --domain djangojs --extension=js,jsx,ts,tsx --locale en
	$(djangoRun) makemessages --domain djangojs --extension=js,jsx,ts,tsx --locale zh_Hans


# i18n 编译翻译后的字符串
i18n-compile:
	$(djangoRun) compilemessages
	$(djangoRun) compilejsi18n
