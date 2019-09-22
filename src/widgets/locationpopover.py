# locationpopover.py
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

from gi.repository import Gtk, GWeather, Gio

_ = GWeather.LocationEntry()

@Gtk.Template(resource_path='/com/github/yursan9/Arkan/ui/locationpopover.ui')
class LocationPopover(Gtk.Popover):
    __gtype_name__ = 'LocationPopover'

    contents = Gtk.Template.Child()
    auto_switch = Gtk.Template.Child()
    loc_entry = Gtk.Template.Child()

    settings = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.github.yursan9.Arkan')

    @Gtk.Template.Callback()
    def on_auto_switch_active(self, switch):
        self.settings.set_boolean('auto-location', self.switch.get_active())

    @Gtk.Template.Callback()
    def on_loc_entry_changed(self, entry):
        loc = self.loc_entry.get_location()

        if loc:
            data = loc.serialize()
            self.settings.set_value('location', data)
