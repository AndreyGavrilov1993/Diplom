# from datetime import datetime, timedelta
# from django.db.models import F
#
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
#
# from mydiplom.my_coworking.cart.models import CartItem
#
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")
#
# @register_job(scheduler, "interval", seconds=3600)
# def delete_ip():
#     for F in CartItem.objects.all():
#         # I assumed here that date_added is time when your object was created
#         time_elapsed = datetime.now() - F.date_added
#         if time_elapsed > timedelta(hours=1):
#            F.delete()
#
# register_events(scheduler)
#
#
#
# # код вернет и удалит все записи, которые были изменены более чем через 1 час после публикации:
#
# CartItem.objects.filter(date_added__gt=F("date_added") + timedelta(hours=1)).delete()
#
# # код вернет и удалит все записи, которые были изменены более чем через 1 день после публикации:
#
# CartItem.objects.filter(date_added__gt=F("date_added") + timedelta(days=1)).delete()
#
# # код вернет и удалит все записи, которые были изменены более чем через 1 месяц после публикации:
#
# CartItem.objects.filter(date_added__gt=F("date_added") + timedelta(days=30)).delete()