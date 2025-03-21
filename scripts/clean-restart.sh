docker-compose down --remove-orphans;
docker system prune --all --volumes -f;
systemctl restart docker;
git clean -fdx -e .env -e active_interview_backend/db/db.sqlite3;
docker-compose up -d --build;
