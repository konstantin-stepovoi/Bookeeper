from typing import Union
from PySide6.QtWidgets import QMessageBox
import datetime


def reorder_time(date: str) -> Union[datetime.datetime, None]:
    """
    Попытка преобразования строки даты в формат datetime.

    Args:
        date (str): Строка с датой
        в формате "ГГГГ-ММ-ДД" или "ДД.ММ.ГГГГ".

    Returns:
        Union[datetime, None]:
        Возвращает объект datetime,
        если удалось преобразовать строку даты,
        иначе возвращает None.
    """
    try:
        expense_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        try:
            day, month, year = map(
                int, date.split('.'))
            expense_date = datetime.datetime(
                year,
                month,
                day)
        except ValueError:
            QMessageBox.warning(
                None,
                'Ошибка',
                'Неверный формат даты. Введите дату в формате "ГГГГ-ММ-ДД".')
            return None
    return expense_date


def date_is_in_range(time: str, year: str, month: str, day: str) -> bool:
    """
    Проверяет, находится ли указанная
    дата в пределах заданного временного диапазона.

    Args:
        time (str): Временной интервал (День, Неделя, Месяц).
        year (str): Год.
        month (str): Месяц.
        day (str): День.
    Returns:
        bool: True, если
        дата находится в указанном
        диапазоне, в противном случае - False.
    """
    this_year, this_month, this_day = map(
        int,
        str(datetime.date.today()).split()[0].split("-"))
    year, month, day = int(year), int(month), int(day)
    if this_year != year:
        return False
    if time == 'Day':
        if this_day == day and this_month == month:
            return True
        else:
            return False
    elif time == 'Week':
        today_date = datetime.date(this_year, this_month, this_day)
        target_date = datetime.date(year, month, day)
        week_start = today_date - datetime.timedelta(days=today_date.weekday())
        week_end = week_start + datetime.timedelta(days=6)
        return week_start <= target_date <= week_end

    elif time == 'Month':
        return this_month == month
