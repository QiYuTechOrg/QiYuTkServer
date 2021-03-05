poetry-django-run:=cd tbk && poetry run python manage.py


local-clean-log:
	rm logs/*.log* || true
	rm logs/api/*.log* || true


local-run-grab-order:
	$(poetry-django-run) grab_order


local-clean-test-user:
	$(poetry-django-run) clean_test_user
