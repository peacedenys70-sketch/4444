# Configuration Gunicorn pour Render
import os

# Nombre de workers : 2 * CPU + 1 (Render free = 1 CPU)
workers = 2
worker_class = 'sync'
timeout = 120
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
accesslog = '-'
errorlog  = '-'
loglevel  = 'info'
