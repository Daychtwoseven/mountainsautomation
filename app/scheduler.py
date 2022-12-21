from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from app.views import *


def start(action):
    if action == "run_all":
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_all, 'interval', minutes=120)
        scheduler.start()


def run_all():
    mst_tz = pytz.timezone("MST")
    date_today_in_mst = datetime.now(mst_tz).date().strftime("%m/%d/%Y")
    url_func = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11, url_12,
                url_13,
                url_14, url_15, url_16, url_17, url_18, url_19, url_20, url_21, url_22, url_23, url_24,
                url_25, url_26, url_27, url_28, url_29, url_30, url_31, url_32, url_33, url_34, url_35,
                url_36, url_37, url_38, url_39, url_40, url_41, url_42, url_43, url_44, url_45, url_46,
                url_47, url_48, url_49, url_50, url_51, url_52, url_53, url_54, url_55, url_56, url_57,
                url_58, url_59, url_60, url_61]

    counter = 0
    threads = []
    for i in Urls.objects.all():
        if i.is_active:
            t = threading.Thread(target=url_func[counter], args=(date_today_in_mst, date_today_in_mst, i))
            t.start()
            threads.append(t)

        counter += 1

    for thread in threads:
        thread.join()
