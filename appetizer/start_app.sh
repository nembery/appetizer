#!/usr/bin/env sh

export HOME=/home/cnc_user
export GIT_SSL_NO_VERIFY=1

python3 /app/src/appetizer/build_app.py

cd /app/cnc || exit 1
celery -A pan_cnc worker --loglevel=info  &
if [ ! -f $HOME/.pan_cnc/db.sqlite3 ];
  then
    python /app/cnc/manage.py migrate && \
    python /app/cnc/manage.py shell -c \
    "from django.contrib.auth.models import User; User.objects.create_superuser('${CNC_USERNAME}','admin@example.com', '${CNC_PASSWORD}')" \
    || exit 1
fi
echo "====="
echo "====="
echo "====="
echo "=================== Welcome to ${CNC_APP} ============================"
echo "====="
echo "====="
echo "====="
python3 /app/cnc/manage.py runserver 0.0.0.0:8080