!/bin/sh

until cd /core
do
    echo "Waiting for server volume..."
done


celery -A Blood_Test_Result worker -l info

