celery -A  CodePedia worker -l info > celerylog.out 2>&1 &
git stash
git pull
sudo service nginx restart