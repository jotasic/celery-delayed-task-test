## 프로젝트 정보

Celery에서 메시지 브로커를 Redis를 사용할 경우 발생할 수 있는 문제에 대해서 테스트를 위한 프로젝트

## 사용법

### 프로젝트 세팅 및 실행 방법

```bash
# 가상 환경 및 파이썬 패키지 설치
conda create -n celery-test python=3.11
conda activate celery-test
pip install -r requirements.txt

# 스크립트 실행 (celery worker 및 flower 실행)
cd app
run_celery.sh 2
```

# 테스트

## eta 테스트

task 실행시 [eta](https://docs.celeryq.dev/en/stable/glossary.html#term-ETA)인자로 날짜 및 시간이 주어지면 해당 시각에 task가 실행 된다.

일반적으로 생각하기에는 그 시간 이후에 실행된다고 생각하지만 그렇지 않다.

왜냐하면 Celery에서 브로커로 Redis사용시 AMQP를 모사해서 작동한다.

그 방법은 visibility timeout 이라는 시간 만큼 시간이 지나면 무조건 실패했다고 가정하고, 다시 message를 보낸다.

eat 값이 너무 크면 해당 task는 중복 실행가능 성이 있다.
visibility timeout 기본 값은 1시간이다.
해당 프로젝트에서는 테스트를 위해 5초로 줄였다.

> AMQP에 대한 보충 설명이 필요함

### 실행 방법

```
# 첫번째 인자는 현재로 부터 실행 시점 (초)
# 두번째 인자는 터미널에 출력하기 위한 값
python manage.py task_eta_test 120 "CELERY"
```

### 결과

실행

```
python manage.py task_eta_test 30 "CELERY"

Successfully Excute Task name: CELERY expected excute time: 2023-07-29 15:22:37.747320
```

worker
하나의 message를 보냈는데, 동일한 task가 실행된 현상

```
[2023-07-29 15:22:07,803] Task tasktest.tasks.run_task[d410ec40-ec2b-4ca5-9bdc-557528565932] received

[2023-07-29 15:22:17,098] Task tasktest.tasks.run_task[d410ec40-ec2b-4ca5-9bdc-557528565932] received

[2023-07-29 15:22:37,757: INFO/ForkPoolWorker-8] [celery@worker2-d410ec40-ec2b-4ca5-9bdc-557528565932]  SUCCESS NAME: CELERY

[2023-07-29 15:22:37,759: INFO/ForkPoolWorker-1] [celery@worker2-d410ec40-ec2b-4ca5-9bdc-557528565932]  SUCCESS NAME: CELERY
```

### 참고

- [Eta 및 countdown](https://docs.celeryq.dev/en/stable/userguide/calling.html#eta-and-countdown)
- [Visibility timeout](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html#id1)
- [Celery ETA Tasks Demystified](https://engineering.instawork.com/celery-eta-tasks-demystified-424b836e4e94)
- [AMQP - 위키백과](https://ko.wikipedia.org/wiki/AMQP)
