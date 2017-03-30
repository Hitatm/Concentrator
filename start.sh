supervisorctl shutdown
supervisord -c /etc/supervisord.conf
sudo gunicorn -c deploy_config.py run:app
