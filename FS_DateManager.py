from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange


def get_date_relative_text(date_from, date_to, date_unit):
    if date_from == date_to:
        date_relative_text = get_date_relative_suffix_text(str(date_from))
        date_unit_text = get_date_unit(date_unit)
        return str(date_relative_text) + " " + str(date_unit_text)
    else:
        (start_date, end_date) = get_date_period(date_from, date_to, date_unit)
        return str(start_date) + ' and ' + str(end_date)


def date_text_last():
    return "last"


def date_text_current():
    return "current"


def date_text_next():
    return "next"


def get_date_relative_suffix_text(date_from):
    switcher = {
        '-1': date_text_last(),
        '0': date_text_current(),
        '1': date_text_next(),
    }

    func = switcher.get(date_from, lambda: "Invalid month")

    return func


def date_text_year():
    return "year"


def date_text_quarter():
    return "quarter"


def date_text_month():
    return "month"


def date_text_week():
    return "week"


def date_text_day():
    return "day"


def get_date_unit(date_unit):
    switcher = {
        'y': date_text_year(),
        'q': date_text_quarter(),
        'm': date_text_month(),
        'w': date_text_week(),
        'd': date_text_day(),
    }

    func = switcher.get(date_unit, lambda: "Invalid month")

    return func



def get_today():
    #return datetime.now()
    return (datetime.now() - timedelta(days=3 * 365))


def get_month_name(date):
    print ("@@FS_DateManager.get_month_name", date)

    return datetime.strptime(date, "%m-%d-%Y").strftime("%B")


def year(date_from, date_to):
    start_date = get_today() + relativedelta(years=date_from)
    end_date = get_today() + relativedelta(years=date_to)
    start_date = start_date.replace(day=1).replace(day=1)
    end_date = end_date.replace(month=12).replace(day=31)
    return start_date.strftime("%m-%d-%Y"), end_date.strftime("%m-%d-%Y")


def quarter(date_from, date_to):
    return None


def month(date_from, date_to):
    start_date = get_today() + relativedelta(months=date_from)
    end_date = get_today() + relativedelta(months=date_to)
    start_date = start_date.replace(day=1)
    (month, last_day_month) = monthrange(end_date.year, end_date.month)
    end_date = end_date.replace(day=last_day_month)

    return start_date.strftime("%m-%d-%Y"), end_date.strftime("%m-%d-%Y")


def week(date_from, date_to):
    #start_date = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7) + relativedelta(weeks=date_from)
    #end_date = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7) + relativedelta(weeks=date_to)
    start_date = get_today() - timedelta(days=get_today().isoweekday() % 7) + relativedelta(weeks=date_from)
    end_date = get_today() - timedelta(days=get_today().isoweekday() % 7) + relativedelta(weeks=date_to)
    end_date = end_date + relativedelta(days=6)

    return start_date.strftime("%m-%d-%Y"), end_date.strftime("%m-%d-%Y")


def day(date_from, date_to):
    start_date = get_today() + relativedelta(days=date_from)
    end_date = get_today() + relativedelta(days=date_to)

    return start_date.strftime("%m-%d-%Y"), end_date.strftime("%m-%d-%Y")


def get_date_period(date_from, date_to, date_unit):
    switcher = {
        'y': year(date_from, date_to),
        'q': quarter(date_from, date_to),
        'm': month(date_from, date_to),
        'w': week(date_from, date_to),
        'd': day(date_from, date_to)
    }

    func = switcher.get(date_unit, lambda: "Invalid month")

    return func


def get_date_slicer(start_date, delta, date_unit):
    s_date = get_today() #datetime.today()
    e_date = get_today #datetime.today()
    start_date = datetime.strptime(start_date, '%m-%d-%Y')
    if date_unit == 'y':
        s_date = (start_date + relativedelta(months=delta)).replace(day=1)
        (month, last_day_month) = monthrange(s_date.year, s_date.month)
        e_date = (s_date.replace(day=last_day_month))

    return s_date.strftime("%m-%d-%Y"), e_date.strftime("%m-%d-%Y")
