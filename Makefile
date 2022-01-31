.PHONY: format
format:
	docker-compose exec backend bash -c "black . && isort ."
	
.PHONY: test
test:
	docker-compose exec backend bash -c "python manage.py test"