PY_FILES := $(shell git ls-files '*.py')

up:
	docker compose up -d --build

clean:
	docker compose down --rmi all

lint:
	pylint $(PY_FILES)

black:
	black $(PY_FILES)
