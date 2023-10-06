alembic_init:
	alembic -c app/migrations/alembic.ini -x db=$(env) revision --autogenerate -m init

alembic_migrate:
	alembic -c app/migrations/alembic.ini -x db=$(env) upgrade head