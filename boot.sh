#!/bin/sh
exec gunicorn -b :${PORT:-5000} --access-logfile - --error-logfile - blogpostapi:app
