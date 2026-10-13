#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-pfsense-qinq-parent-if}"
export PYTHONUNBUFFERED=1

LABEL="PFSENSE-QINQ-PARENT-IF"
WITNESS="PFSENSE-QINQ-PARENT-IF-WITNESS"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  down
  exit 1
}

trap down EXIT

echo "== docker compose down (clean) =="
down
trap down EXIT

if ! docker image inspect php:8.3-cli-bookworm >/dev/null 2>&1; then
  echo "== docker pull php:8.3-cli-bookworm =="
  docker pull php:8.3-cli-bookworm || fail_setup "php-image-pull-failed"
fi

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 5); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 8
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait for 127.0.0.1:18810 =="
ok=0
for i in $(seq 1 60); do
  if python3 - <<'PY'
import socket
sock = socket.create_connection(("127.0.0.1", 18810), 2)
sock.close()
PY
  then
    ok=1
    echo "lab-ready attempt=${i}"
    break
  fi
  echo "lab-wait attempt=${i}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 || true
  fail_setup "lab-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
