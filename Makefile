api_container_name=student_helper.telegram

make_migration:
	docker exec -it $(api_container_name) alembic revision --autogenerate -m '$(message)'

migrate:
	docker exec -it $(api_container_name) alembic upgrade head