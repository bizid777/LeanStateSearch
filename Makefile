.PHONY: fmt lint dev-fe start-be build-images init-service proto clean

FRONTEND = lean-state-search
BACKEND = state-search-be

fmt:
	(cd protos && buf format -w)
	(cd ${FRONTEND} && prettier . -w )
	(cd ${BACKEND} && ruff format .)

lint:
	(cd ${BACKEND} && ruff check .)
	(cd protos && buf lint)
	(cd ${FRONTEND} && pnpm lint)

dev-fe:
	(cd ${FRONTEND} && PORT=${FRONTEND_PORT} pnpm run dev)

# Run backend in background; logs are written to /tmp/lean_state_search.log
run-be:
	(cd ${BACKEND} && uv run python -m state_search_be.run_be > /tmp/lean_state_search.log 2>&1 &)

# Legacy target kept for compatibility
start-be: run-be

build-images:
	(cd ${FRONTEND} && MODE=docker docker build -t ${FRONTEND}:latest .)
	(cd ${BACKEND} && MODE=docker docker build -t ${BACKEND}:latest .)

init-service:
	(docker compose up --wait)
	(sleep 5 && ./scripts/init-pg.sh)
	(cd ${BACKEND} && poetry install && poetry run prisma db push)

proto:
	(cd protos && buf generate)
	(cd ${FRONTEND} && pnpm i && rm -rf lib/gen && pnpm exec buf generate ../protos/state_search/v1/state_search.proto)

clean:
	(cd scripts/ && docker-compose down && docker-compose rm -f)