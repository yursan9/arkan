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

from gi.repository import Gtk, Handy
from .shalatlistrow import ShalatListRow
Handy.init()


@Gtk.Template(resource_path='/com/github/yursan9/Arkan/ui/shalatlist.ui')
class ShalatList(Handy.Column):
    __gtype_name__ = 'ShalatList'

    listbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.listbox.set_header_func(self._add_separator)

    def populate(self, data):
        self.listbox.foreach(lambda widget: widget.destroy())

        for key in data:
            time = data[key].strftime('%H:%M')
            row = ShalatListRow(key, time)
            self.listbox.add(row)

    def to_column(self):
        self.set_border_width(18)
        self.set_halign(Gtk.Align.FILL)
        self.listbox.get_style_context().remove_class('sidebar')
        self.listbox.get_style_context().add_class('frame')

    def to_sidebar(self):
        self.set_border_width(0)
        self.set_halign(Gtk.Align.START)
        self.listbox.get_style_context().remove_class('sidebar')
        self.listbox.get_style_context().add_class('frame')

    def _add_separator(self, row, before):
        # Before is none, for the first row
        if before is None:
            row.set_header(None)
            return

        current = row.get_header()
        if current is None:
            current = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            row.set_header(current)
