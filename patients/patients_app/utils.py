from .models import Event
from calendar import HTMLCalendar
from datetime import datetime, timedelta, time

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        date = f'{self.year}-{self.month}-{day}'
        events_per_day = events.filter(start_time__day=day)
        events_per_day = events_per_day.order_by('start_time')
        occupied_hours = []
        d = ''
        hours = [('9:00', '19:00', 'free')]
        for event in events_per_day:
            visit_time_start = event.start_time.strftime('%H:%M')
            visit_time_end = event.end_time.strftime('%H:%M')
            occupied_hours.append((visit_time_start, visit_time_end))
        if len(events_per_day) > 1:
            hours = schedule(occupied_hours)
        elif len(events_per_day) == 1:
            hours = [('9:00', occupied_hours[0][0], 'free'), (occupied_hours[0][0], occupied_hours[0][1]), (occupied_hours[0][1], '19:00', 'free')]
            hours = adjust_schedule(hours)

        hours_events = []
        occupied_dct = {hour:event for hour, event in zip(occupied_hours, events_per_day)}
        for hour in hours:
            if hour not in occupied_dct:
                hours_events.append((hour, None))
            else:
                hours_events.append((hour, occupied_dct[hour]))

        for hour, event in hours_events:
            if len(hour) == 2:
                d += f'<li style="list-style-type: none; margin-bottom: 1px; background-color:#05445E; padding: 3px; border: 0px solid black; border-radius: 0.3em 0.3em 0.3em 0.3em;"><button onclick="location.href=\'update_event/{event.id}/\';" style="background-color:#05445E; color: #E3FCFF; border:none; cursor:pointer;"> {hour[0]} - {hour[1]} </button></li>'
            else:
                d += f'<li style="list-style-type: none; margin-bottom: 1px; font-style: italic; background-color:#03293935; padding: 3px;  border: 0px solid black; border-radius: 0.3em 0.3em 0.3em 0.3em;">{hour[0]} - {hour[1]} free </li>'
        if day != 0:
            return f"<td style='border-radius: 0.8em;border: 0px;background-color: #B9DCDF;'><a href='events/{date}' style='color: #248b81 !important; text-decoration: none;' class='date'>{day}</a><ul> {d} </ul></td>"
        return '<td style="border-radius: 0.8em; border: 0px; background-color: #B9DCDF;"></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True, request=None):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, user=request.user)
        cal = f'<table style="border-spacing: 10px;border-collapse: separate;" border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

def adjust_schedule(occupied_slots):
    result = occupied_slots[:]
    for visit in occupied_slots:
        hour1 = int(visit[0].split(':')[0])
        hour2 = int(visit[1].split(':')[0])
        minute1 = int(visit[0].split(':')[1])
        minute2 = int(visit[1].split(':')[1])
        if hour1 == hour2:
            if minute2 - minute1 < 30 and 'free' in visit:
                result.remove(visit)
        elif hour2 - hour1 == 1:
            if minute2 + 60 - minute1 < 30 and 'free' in visit:
                result.remove(visit)
    return result


def schedule(occupied_slots):
    result = []
    sort_values = {}
    free_slots = [('9:00', occupied_slots[0][0])] + [(occupied_slots[i][1], occupied_slots[i+1][0]) for i in range(len(occupied_slots)-1)] + [(occupied_slots[-1][1], '19:00')]

    free_slots = [(start, end) for start, end in free_slots]
    result = occupied_slots + free_slots
    for i in result:
        sort_values[i[0]] = int(''.join(i[0].split(':')))
    result = sorted(result, key=lambda x: sort_values[x[0]])
    for i, x in enumerate(result):
        if x in free_slots:
            result[i] = list(x) + ['free']
            result[i] = tuple(result[i])
        if '19:00' in result[i] and 'free' not in result[i]:
            result.pop()
    result = adjust_schedule(result)
    return result
