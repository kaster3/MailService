run:  # run application with gunicorn and uvicorn with the prepared config
	poetry run gunicorn main:main_app --worker-class uvicorn.workers.UvicornWorker -c infra/gunicorn.conf.py