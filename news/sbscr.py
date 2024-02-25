import schedule
import time
from news.utils import send_weekly_newsletter


def send_newsletter():
    send_weekly_newsletter()


schedule.every().monday.at("09:00").do(send_newsletter)

while True:
    schedule.run_pending()
    time.sleep(60)
