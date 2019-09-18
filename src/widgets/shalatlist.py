# shalatlist.py
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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')

from gi.repository import Gtk, Handy
Handy.init()

from .shalatlistrow import ShalatListRow

@Gtk.Template(resource_path='/com/github/yursan9/Arkan/ui/shalatlist.ui')
class ShalatList(Handy.Column):
    __gtype_name__ = 'ShalatList'

    listbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def populate(self):
        example = [
            {'name': 'Fajr', 'time': '04:45'},
            {'name': 'Zuhr', 'time': '12:00'},
            {'name': 'Ashr', 'time': '15:15'},
            {'name': 'Maghrib', 'time': '18:45'},
            {'name': 'Isya', 'time': '19:05'},
        ]

        for x in example:
            row = ShalatListRow(x['name'], x['time'])
            self.listbox.add(row)