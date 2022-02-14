from time import time
from plyer import notification
from datetime import datetime
import sched
import time

def schedule(message, hour, mins, day, month, year, priority):
    remind_mssg=message
    in_year=int(year)
    in_month=int(month)
    in_day=int(day)
    in_hour=int(hour)
    in_min=int(mins)
    priority=int(priority)
    msg=""
    def notif_schedule(mss):
        notification.notify(
            title = remind_mssg,
        	message = mss,
            app_icon = "C:\\Users\\acer\\Documents\\Notification Reminder Python\\notif.ico",
    	    timeout = 10,
	    )

    now = datetime.now()
    year_now = now.strftime("%Y")
    month_now = now.strftime("%m")
    day_now = now.strftime("%d")
    hour_now = now.strftime("%H")
    minutes_now = now.strftime("%M")
    sec_now = now.strftime("%S")
    year_diff = in_year-int(year_now)
    month_diff = in_month-int(month_now)
    day_diff = in_day-int(day_now)
    hour_diff = in_hour-int(hour_now)
    min_diff = in_min-int(minutes_now)

    in_sec = int(year_diff * 365 * 24 * 60 * 60 + month_diff * 30 *24 * 60 * 60 + day_diff * 24 * 60 * 60 + hour_diff * 60 * 60 + min_diff * 60 - int(sec_now))

    scheduler = sched.scheduler(time.time, time.sleep)
    
    if priority == 1:
        scheduler.enter(in_sec, 1, notif_schedule, (' ', ))

    elif priority == 2:

        if in_sec >= 2592000:
            scheduler.enter(in_sec - 30 * 24 * 60 * 60, 1, notif_schedule, ('1 month left', ))
            scheduler.enter(in_sec - 24*60*60, 1, notif_schedule, ('1 day left', ))
            scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
        else:
            if in_sec >= 86400:
                scheduler.enter(in_sec - 24 * 60 * 60, 1, notif_schedule, ('1 day left', ))
                scheduler.enter(in_sec - 60 * 60, 1, notif_schedule, ('1 hour left', ))
                scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
            else:
                if in_sec >= 3600:
                    scheduler.enter(in_sec - 15 * 60, 1, notif_schedule, ('15 mins left', ))
                    scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
                else:
                    if in_sec > 300:
                        scheduler.enter(in_sec - 5 * 60, 1, notif_schedule, ('5 mins left', ))
                        scheduler.enter(in_sec,1,notif_schedule, (' ', ))    
                    else: 
                        scheduler.enter(in_sec, 1, notif_schedule, (' ', ))

    elif priority == 3 or priority == 4:

        if in_sec > 2592000:
            scheduler.enter(in_sec - 30 * 24 * 60 * 60, 1, notif_schedule, ('30 days left', ))
            scheduler.enter(in_sec - 15 * 24 * 60 * 60, 1, notif_schedule, ('15 days left', ))
            scheduler.enter(in_sec - 24 * 60 * 60, 1, notif_schedule, ('1 day left', ))
            scheduler.enter(in_sec - 60 * 60, 1, notif_schedule, ('1 hour left', ))
            scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
        else:
            if in_sec > 86400:
                scheduler.enter(in_sec - 24 * 60 * 60, 1, notif_schedule, ('1 day left', ))
                scheduler.enter(in_sec - 12 * 60 * 60, 1, notif_schedule, ('12 hour left', ))
                scheduler.enter(in_sec - 60 * 60, 1, notif_schedule, ('1 hour left', ))
                scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
            else:
                if in_sec > 3600:
                    scheduler.enter(in_sec - 15 * 60, 1, notif_schedule, ('15 mins left', ))
                    scheduler.enter(in_sec - 30 * 60, 1, notif_schedule, ('30 mins left', ))  
                    scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
                else:
                    if in_sec > 1800:
                        scheduler.enter(in_sec - 15 * 60, 1, notif_schedule, ('15 mins left', ))
                        scheduler.enter(in_sec - 5 * 60, 1, notif_schedule, ('5 mins left', ))
                        scheduler.enter(in_sec,1,notif_schedule, (' ', ))  
                    else:
                        if in_sec > 300:
                            scheduler.enter(in_sec - 5 * 60, 1, notif_schedule, ('5 mins left', ))
                            scheduler.enter(in_sec,1,notif_schedule, (' ', ))    
                        else:               
                            scheduler.enter(in_sec, 1, notif_schedule, (' ', ))
                           
    scheduler.run()

def notificationn():
    with open('database_files\\tasks_db.txt', 'r') as database:
        line = database.readlines()
    
        index = int(line[-1][3])-1
        semi_colon = line[index].index(";")
        msg = line[index][5 : semi_colon]
        hour = line[index][-19 : -17]
        minutes = line[index][-16 : -14]
        day = line[index][-13 : -11]
        month = line[index][-10 : -8]
        year = line[index][-7 : -3]
        priority = line[index][-2]
        
        schedule(msg, hour, minutes, day, month, year, priority)
notificationn()