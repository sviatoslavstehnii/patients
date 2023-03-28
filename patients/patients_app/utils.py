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
        for i in hours:
            if len(i) == 2:
                d += f'<li style="list-style-type: none; background-color:#189AB4; padding: 3px; border-radius: 0.3em 0.3em 0.3em 0.3em;"> {i[0]} - {i[1]} </li>'
            else:
                d += f'<li style="list-style-type: none; background-color:#03293972; padding: 3px; border-radius: 0.3em 0.3em 0.3em 0.3em;"> {i[0]} - {i[1]} free</li>'
        if day != 0:
            return f"<td><a href='events/{day}' class='date' style='color: #E3FCFF !important;'>{day}</a><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


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

    return result
