.PHONY:
.SILENT:
.DEFAULT_GOAL := run


args = "$(filter-out $@,$(MAKECMDGOALS))"

build:
	docker-compose -f docker-compose.yml up --build

up:
	docker-compose -f docker-compose.yml up

down:
	docker-compose -f docker-compose.yml down

migrations:
	 docker exec -it amanat python3 manage.py makemigrations

migrate:
	docker exec -it amanat python3 manage.py migrate

app:
	docker exec -it amanat python3 manage.py startapp $(call args)

prune:
	docker system prune

shell:
	python manage.py shell_plus