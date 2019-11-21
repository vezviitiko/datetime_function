#!/usr/bin/python3
#coding=UTF-8
__author__ = "KomissarovAV"
__author__ = "Matt Davis"

'''
					Оглавление

	create_datetime_item       -   формирование данных даты для заданного дня
	create_datetime_item_hour  -   формирование данных даты для заданного дня от часа
	week_seconds_to_utc        -   перевод gps недели в datetime  в формате UTC
	epoch_date	               -   формирование даты от исходных входных параметров      
	date_to_gps_week           -   определение gps недели по дате
    datatime_conv              -   переформатирование строки в дату 
    datetime_timedelta         -   определение разницы между датами
    roundTime                  -   округление даты
    datetime_To_seconds
    date_to_jd
    jd_to_date
    hmsm_to_days
    days_to_hmsm
    datetime_to_jd
    jd_to_datetime
    timedelta_to_days
    mjd_to_jd
    jd_to_mjd
'''

import time, math
import datetime, calendar

def create_datetime_item(days_d=0):
	now_date = datetime.datetime.now()
	now_date = now_date - datetime.timedelta(days=days_d)
	
	year 	 = now_date.strftime('%Y')
	month 	 = now_date.strftime('%m')
	day 	 = now_date.strftime('%d')
	day_year = now_date.strftime('%j')
	hour 	 = now_date.strftime('%H')

	return year, month, day, day_year, hour, now_date


def create_datetime_item_hour(hour=0):
	now_date = datetime.datetime.now()
	now_date = now_date - datetime.timedelta(hours=hour)
	
	year 	 = now_date.strftime('%Y')
	month 	 = now_date.strftime('%m')
	day 	 = now_date.strftime('%d')
	day_year = now_date.strftime('%j')
	hour 	 = now_date.strftime('%H')

	hour_b_arr = 'abcdefghijklmnopqrstuvwx'
	hour_b 	 = hour_b_arr[int(hour)]

	return year, month, day, day_year, hour, hour_b, now_date


def week_seconds_to_utc(gpsweek,gpsseconds):
	
	datetimeformat = "%Y-%m-%d %H:%M:%S"
	epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
	elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds))
	return(datetime.datetime.strftime(epoch + elapsed,datetimeformat))


def datatime_conv(datatime):
    if isinstance(datatime, str):
        datatime = str_to_datetime(datatime)
    return datatime


def epoch_date(trtime,year,month,day):
	s = '%(number)02d' % {'number' : trtime%60}
	if int(s) > 60:
		s = '60'
	elif int(s) < 0:
		s = '00'
	
	m = '%(number)02d' % {'number' : (trtime//60)%60}
	if int(m) > 60:
		m = '60'
	elif int(m) < 0:
		m = '00'
	
	h = '%(number)02d' % {'number' : trtime//3600}
	if int(h) > 23:
		h = '23'
	elif int(h) < 0:
		h = '00'
	
	epoch = str('{0}-{1}-{2} {3}:{4}:{5}'.format(year,'%02i' % int(month),'%02i' % int(day), h,m,s))
	return epoch   


def date_to_gps_week(year,month,day):
	secsInWeek = 604800 
	epochTuple = (1980, 1, 6, 0, 0, 0) + (-1, -1, 0) 
	
	t0 = time.mktime(epochTuple) 
	t  = time.mktime((int(year),int(month),int(day), 0, 0, 0, -1, -1, 0)) 
	t  = t + 14
	tdiff = t - t0 
	noWeeks = int(math.floor(tdiff/secsInWeek))
	return noWeeks


def str_to_datetime(datetime_str):
	#from datetime import datetime
	return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


def datetime_timedelta(datetime1, datetime2):
	if datetime1 > datetime2:
		return datetime1 - datetime2
	else:
		return datetime2 - datetime1


def roundTime(dt=None, roundTo=60):
	"""
	Round a datetime object to any time lapse in seconds
	dt : datetime.datetime object, default now.
	roundTo : Closest number of seconds to round to, default 1 minute.
	Author: Thierry Husson 2012 - Use it as you want but don't blame me.
	
	Example:
		roundTo=30*60 - 30 minutes
		
	"""
	if dt == None : dt = datetime.datetime.now()
	seconds = (dt.replace(tzinfo=None) - dt.min).seconds
	rounding = (seconds+roundTo/2) // roundTo * roundTo
	return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


def datetime_To_seconds(dt):
	
	dt_secunds = time.mktime(dt.timetuple())
	
	return dt_secunds


def date_to_jd(year,month,day):
    """
    Convert a date to Julian Day.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
    
    Returns
    -------
    jd : float
        Julian Day
        
    Examples
    --------
    Convert 6 a.m., February 17, 1985 to Julian Day
    
    >>> date_to_jd(1985,2,17.25)
    2446113.75
    
    """
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
        
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
        
    D = math.trunc(30.6001 * (monthp + 1))
    
    jd = B + C + D + day + 1720994.5
    
    return jd
    
    
def jd_to_date(jd):
    """
    Convert Julian Day to date.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    jd : float
        Julian Day
        
    Returns
    -------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
        
    Examples
    --------
    Convert Julian Day 2446113.75 to year, month, and day.
    
    >>> jd_to_date(2446113.75)
    (1985, 2, 17.25)
    
    """
    jd = jd + 0.5
    
    F, I = math.modf(jd)
    I = int(I)
    
    A = math.trunc((I - 1867216.25)/36524.25)
    
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
        
    C = B + 1524
    
    D = math.trunc((C - 122.1) / 365.25)
    
    E = math.trunc(365.25 * D)
    
    G = math.trunc((C - E) / 30.6001)
    
    day = C - E + F - math.trunc(30.6001 * G)
    
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
        
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
        
    return year, month, day
    
    
def hmsm_to_days(hour=0,min=0,sec=0,micro=0):
    """
    Convert hours, minutes, seconds, and microseconds to fractional days.
    
    Parameters
    ----------
    hour : int, optional
        Hour number. Defaults to 0.
    
    min : int, optional
        Minute number. Defaults to 0.
    
    sec : int, optional
        Second number. Defaults to 0.
    
    micro : int, optional
        Microsecond number. Defaults to 0.
        
    Returns
    -------
    days : float
        Fractional days.
        
    Examples
    --------
    >>> hmsm_to_days(hour=6)
    0.25
    
    """
    days = sec + (micro / 1.e6)
    
    days = min + (days / 60.)
    
    days = hour + (days / 60.)
    
    return days / 24.
    
    
def days_to_hmsm(days):
    """
    Convert fractional days to hours, minutes, seconds, and microseconds.
    Precision beyond microseconds is rounded to the nearest microsecond.
    
    Parameters
    ----------
    days : float
        A fractional number of days. Must be less than 1.
        
    Returns
    -------
    hour : int
        Hour number.
    
    min : int
        Minute number.
    
    sec : int
        Second number.
    
    micro : int
        Microsecond number.
        
    Raises
    ------
    ValueError
        If `days` is >= 1.
        
    Examples
    --------
    >>> days_to_hmsm(0.1)
    (2, 24, 0, 0)
    
    """
    hours = days * 24.
    hours, hour = math.modf(hours)
    
    mins = hours * 60.
    mins, min = math.modf(mins)
    
    secs = mins * 60.
    secs, sec = math.modf(secs)
    
    micro = round(secs * 1.e6)
    
    return int(hour), int(min), int(sec), int(micro)
    

def datetime_to_jd(date):
    """
    Convert a `datetime.datetime` object to Julian Day.
    
    Parameters
    ----------
    date : `datetime.datetime` instance
    
    Returns
    -------
    jd : float
        Julian day.
        
    Examples
    --------
    >>> d = datetime.datetime(1985,2,17,6)  
    >>> d
    datetime.datetime(1985, 2, 17, 6, 0)
    >>> jdutil.datetime_to_jd(d)
    2446113.75
    
    """
    days = date.day + hmsm_to_days(date.hour,date.minute,date.second,date.microsecond)
    
    return date_to_jd(date.year,date.month,days)
    
    
def jd_to_datetime(jd):
    from datetime import datetime
    """
    Convert a Julian Day to an `jdutil.datetime` object.
    
    Parameters
    ----------
    jd : float
        Julian day.
        
    Returns
    -------
    dt : `jdutil.datetime` object
        `jdutil.datetime` equivalent of Julian day.
    
    Examples
    --------
    >>> jd_to_datetime(2446113.75)
    datetime(1985, 2, 17, 6, 0)
    
    """
    year, month, day = jd_to_date(jd)
    
    frac_days,day = math.modf(day)
    day = int(day)
    
    hour,min,sec,micro = days_to_hmsm(frac_days)
    
    return datetime(year,month,day,hour,min,sec,micro)


def timedelta_to_days(td):
    """
    Convert a `datetime.timedelta` object to a total number of days.
    
    Parameters
    ----------
    td : `datetime.timedelta` instance
    
    Returns
    -------
    days : float
        Total number of days in the `datetime.timedelta` object.
        
    Examples
    --------
    >>> td = datetime.timedelta(4.5)
    >>> td
    datetime.timedelta(4, 43200)
    >>> timedelta_to_days(td)
    4.5
    
    """
    seconds_in_day = 24. * 3600.
    
    days = td.days + (td.seconds + (td.microseconds * 10.e6)) / seconds_in_day
    
    return days

def mjd_to_jd(mjd):
    """
    Convert Modified Julian Day to Julian Day.
        
    Parameters
    ----------
    mjd : float
        Modified Julian Day
        
    Returns
    -------
    jd : float
        Julian Day
    
        
    """
    return mjd + 2400000.5

def jd_to_mjd(jd):
    """
    Convert Julian Day to Modified Julian Day
    
    Parameters
    ----------
    jd : float
        Julian Day
        
    Returns
    -------
    mjd : float
        Modified Julian Day
    
    """
    jd = jd - 2400000.5
    return jd
