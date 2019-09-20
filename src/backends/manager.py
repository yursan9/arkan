# manager.py
#
# Copyright 2019 Yurizal Susanto <yursan9@pm.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject, GLib

from pathlib import Path
from datetime import datetime

import requests
import json

CACHE_FILE = 'shalat_time.json'

class Manager(GObject.Object):
    filename = None
    shalat_times = {}
    sunmoon_times = {}
    hijri_date = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = Path(GLib.get_user_cache_dir())
        self.filename = self.filename / CACHE_FILE

    def update_with_location(self, city, country):
        now = datetime.today()
        payload = {'method': '3', 'city': city, 'country': country, 'month': now.month, 'year': now.year}
        r = requests.get('http://api.aladhan.com/v1/calendarByCity', params=payload)

        self._save(r.text)
        self._populate(r.json())

    def _save(self, text):
        with self.filename.open('w') as f:
            f.write(text)

    def _populate(self, data=None):
        if not data:
            with self.filename.open() as f:
                data = json.load(f)

        now = datetime.today()

        schedule = data['data'][now.day - 1]
        self._get_times(now, schedule['timings'])
        self._get_hijri_date(schedule['date']['hijri'])

    def _get_times(self, now, data):
        times = {}
        for key in data:
            time = data[key]
            time = time.split()[0]
            time = datetime.strptime(time, '%H:%M')
            time = time.replace(year=now.year, month=now.month, day=now.day)

            times[key] = time

        for key in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
            self.shalat_times[key] = times[key]

        for key in ['Sunrise', 'Sunset', 'Midnight']:
            self.sunmoon_times[key] = times[key]

    def _get_hijri_date(self, data):
        self.hijri_date = "{} {} {}".format(data['day'], data['month']['en'], data['year'])

    def get_current_shalat(self):
        now = datetime.now()

        if self.times['Fajr'] < now <= self.times['Sunrise']:
            return 'Fajr'
        elif self.times['Sunrise'] < now <= self.times['Dhuhr']:
            return 'Dhuhr'
        elif self.times['Dhuhr'] < now <= self.times['Asr']:
            return 'Asr'
        elif self.times['Asr'] < now <= self.times['Maghrib']:
            return 'Maghrib'
        elif self.time['Maghrib'] < now <= self.times['Isha']:
            return 'Isha'

    def get_shalat_times(self):
        return self.shalat_times

    def get_sunmoon_times(self):
        return self.sunmoon_times

    def get_hijri_date(self):
        return self.hijri_date
