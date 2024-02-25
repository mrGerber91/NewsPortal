
from datetime import datetime
import pytz


def real_time(request):
    # Здесь можно установить желаемый город
    city = 'Europe/Moscow'

    # Получаем текущее время в выбранном городе
    real_time = datetime.now(pytz.timezone(city))

    return {'real_time': real_time}
