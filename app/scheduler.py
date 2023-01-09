from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from app.views import *


def start(action):
    if action == "run_all":
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_all, 'interval', minutes=500)
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
                url_58, url_59, url_60, url_61, url_62, url_63, url_64, url_65, url_66, url_67, url_68,
                url_69, url_70,
                url_71, url_72, url_73, url_74, url_75, url_76, url_77, url_78, url_79, url_80, url_81,
                url_82, url_83,
                url_84, url_85, url_86, url_87, url_88, url_89, url_90, url_91, url_92, url_93, url_93,
                url_94, url_95, url_96, url_97, url_98, url_99, url_100, url_101, url_102, url_103, url_104,
                url_105, url_106, url_107, url_108, url_109, url_110, url_111, url_112, url_113, url_114, url_115,
                url_116, url_117, url_118]

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
