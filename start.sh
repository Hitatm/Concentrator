#gunicorn -w 4 -b 0.0.0.0:8000 --access-logfile /tmp/Gunicorn_access.log --access-logformat "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s" --error-logfile /tmp/Gunicorn_debug.log  --log-level info   run:app
gunicorn -w 4 -b 0.0.0.0:8000 -c deploy_config.py run:app
