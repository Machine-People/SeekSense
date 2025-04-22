# for frontend
# cd ../Frontend
# npm run dev
# for backend
python3 -m venv venv
sudo systemctl start redis
sudo docker run --name redis-cache -p 6379:6379 -d redis
python3 run.py
