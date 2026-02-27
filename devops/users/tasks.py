from celery import shared_task
from devops.users.services import profile_count_update

@shared_task
def hello2 ():
    print("hi my world")

    ...

@shared_task
def profile_update():
    profile_count_update()