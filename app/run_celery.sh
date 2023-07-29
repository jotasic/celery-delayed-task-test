#!/bin/bash

# 인자로 받은 워커 수
worker_count=$1

# 인자가 제공되지 않았거나 숫자가 아닌 경우 에러 메시지를 출력하고 종료
if ! [[ "$worker_count" =~ ^[0-9]+$ ]]; then
  echo "Usage: $0 <number_of_workers>"
  exit 1
fi

# 워커 수만큼 셀러리 워커 실행
for i in $(seq 1 $worker_count); do
  celery -A app  worker --loglevel=info -n "worker$i" &
done

# flower 실행
celery -A app flower

# 모든 워커 프로세스가 종료될 때까지 기다림
wait
