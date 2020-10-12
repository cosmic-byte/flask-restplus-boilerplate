.ONESHELL:

.PHONY: clean install tests run all

initdb:
	virtualenv venv; \
	. venv/bin/activate; \
    python manage.py db init; \
    python manage.py db migrate --message 'initial database migration'; \
    python manage.py db upgrade

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	virtualenv venv; \
	. venv/bin/activate; \
	pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple sklearn

tests:
	. venv/bin/activate; \
	python manage.py test

run:
	. venv/bin/activate; \
	python manage.py run

all: clean install tests run
