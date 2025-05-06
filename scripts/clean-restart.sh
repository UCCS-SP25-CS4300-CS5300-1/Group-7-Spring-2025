docker compose down --remove-orphans;
docker system prune --all --volumes -f;
launchctl start docker;
git clean -fdx -e .env -e db -e media;
docker compose up -d --build;
