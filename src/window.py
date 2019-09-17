# window.py
#
# Copyright 2019 Yurizal Susanto
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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')

from gi.repository import Gtk, Handy
Handy.init()

from .widgets.shalatlist import ShalatList

@Gtk.Template(resource_path='/com/github/yursan9/Arkan/ui/window.ui')
class Window(Gtk.ApplicationWindow):
    __gtype_name__ = 'Window'

    contents = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        shalat_list = ShalatList()
        shalat_list.populate()
        self.contents.add(shalat_list)

        self.show_all()
