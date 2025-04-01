Demo to leaern git and github and creating repository for my mad 2 project
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:23f3001764/delte.git
git push -u origin main

backend setting
cd backend
python3 -m venv venv
pip install -r requirements.txt

for maihog
cd ..
 ~/go/bin/MailHog
 in linux to run the server

for redis
ps aux | grep 
sudo kill -9 950 or
redis-cli shutdown
start : redis-server

sudo systemctl stop redis
sudo lsof -i :6379


celery -A app beat --detach
celery -A app worker --detach
celery -A app worker --loglevel=info

celery -A app beat --loglevel=info
celery -A app.celery worker --loglevel=info