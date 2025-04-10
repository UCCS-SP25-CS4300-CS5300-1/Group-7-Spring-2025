docker compose down --remove-orphans;
docker system prune --all --volumes -f;
launchctl start docker;
git clean -fdx -e .env -e active_interview_backend/db -e /active_interview_backend/media;
docker compose up -d --build;
