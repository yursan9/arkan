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
from .widgets.shalatoverview import ShalatOverview
from .backends.manager import Manager

@Gtk.Template(resource_path='/com/github/yursan9/Arkan/ui/window.ui')
class Window(Gtk.ApplicationWindow):
    __gtype_name__ = 'Window'

    contents = Gtk.Template.Child()
    prev_btn = Gtk.Template.Child()
    place_btn = Gtk.Template.Child()
    refresh_btn = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()

    shalat_list = None
    shalat_overview = None

    manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.manager = Manager()
        self.manager.update_with_location('Jakarta', 'Indonesia')

        self.shalat_list = ShalatList()
        self.shalat_list.populate(self.manager.get_shalat_times())
        self.contents.add(self.shalat_list)
        self.contents.child_set(self.shalat_list, name='listview')

        self.shalat_overview = ShalatOverview()
        self.contents.add(self.shalat_overview)
        self.contents.child_set(self.shalat_overview, name='overview')

        self.shalat_overview.connect('change_view', self.on_change_view)

        self.normal_header()
        self.show_all()

    def list_header(self):
        self.place_btn.hide()
        self.refresh_btn.hide()
        self.prev_btn.show()

    def normal_header(self):
        self.header_bar.set_subtitle(self.manager.get_hijri_date())
        self.place_btn.show()
        self.refresh_btn.show()
        self.prev_btn.hide()

    @Gtk.Template.Callback()
    def on_contents_folded(self, widget, param):
        folded = self.contents.get_property(param.name)

        if folded:
            self.contents.set_visible_child_name('overview')
            self.shalat_overview.to_column()
            self.shalat_list.to_column()
        else:
            self.shalat_list.to_sidebar()
            self.shalat_overview.to_view()
            self.normal_header()

    @Gtk.Template.Callback()
    def on_contents_visible_change(self, widget, param):
        view = self.contents.get_property(param.name)

        if view == self.shalat_list:
            self.list_header()
        elif view == self.shalat_overview:
            self.normal_header()

    @Gtk.Template.Callback()
    def on_prev_btn_clicked(self, widget):
        self.contents.set_visible_child(self.shalat_overview)

    def on_change_view(self, widget):
        self.contents.set_visible_child(self.shalat_list)
