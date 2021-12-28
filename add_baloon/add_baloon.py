#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio

import gettext
import os
import sys

textdomain = 'gimp30-std-plug-ins'
gettext.bindtextdomain(textdomain, Gimp.locale_directory())
gettext.bind_textdomain_codeset(textdomain, 'UTF-8')
gettext.textdomain(textdomain)
_ = gettext.gettext
def N_(message): return message

class AddBaloon(Gimp.PlugIn):
    def do_query_procedures(self):
        self.set_translation_domain(textdomain,
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return [ "plug-in-add-baloon" ]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                       Gimp.PDBProcType.PLUGIN,
                                       self.run, None)

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask (Gimp.ProcedureSensitivityMask.DRAWABLE)

        procedure.set_menu_label(N_("Add Baloon..."))
        procedure.set_icon_name(GimpUi.ICON_GEGL)
        procedure.add_menu_path('<Image>/Select')

        procedure.set_documentation(N_("Add a text for baloon"),
                                    N_("Add text and a layer with white inside the selection"),
                                    name)
        procedure.set_attribution("Z-UO", "Z-UO", "2022")

        return procedure

    def run(self, procedure, run_mode, image, n_drawables, drawables, args, run_data):
        if n_drawables != 1:
            msg = _("Procedure '{}' only works with one drawable.").format(procedure.get_name())
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)
        else:
            drawable = drawables[0]

        if run_mode == Gimp.RunMode.INTERACTIVE:
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gdk

            GimpUi.init("add_baloon.py")

            dialog = GimpUi.Dialog(use_header_bar=True,
                                   title=_("Add Baloon)"),
                                   role="add_baloon-Python3")
            dialog.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("_OK"), Gtk.ResponseType.OK)

            geometry = Gdk.Geometry()
            geometry.min_aspect = 0.5
            geometry.max_aspect = 1.0
            dialog.set_geometry_hints(None, geometry, Gdk.WindowHints.ASPECT)

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            dialog.get_content_area().add(box)
            box.show()

            # Label text content
            label = Gtk.Label(label='Text:')
            box.pack_start(label, False, False, 1)
            label.show()

            # scroll area for text
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_vexpand (True)
            box.pack_start(scrolled, True, True, 1)
            scrolled.show()

            # text content box
            text_content = Gtk.TextView()
            contents = 'text'
            buffer = text_content.get_buffer()
            buffer.set_text(contents, -1)
            scrolled.add(text_content)
            text_content.show()

            # TODO select font

            # TODO select font-size

            # TODO add spinner for waiting

            while (True):
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    # TODO enable spinner and lock all other values

                    # ERROR add new trasparent layer
                    overlay_layer = Gimp.Layer.new(
                        image, 'hide_background',
                        drawable.get_width(), drawable.get_height(),
                        Gimp.ImageType, 100.0,
                        Gimp.LayerMode.NORMAL
                    )
                    overlay_layer.fill(Gimp.FillType.TRANSPARENT)

                    # TODO add white fill following the selection

                    # TODO add text layer

                    # TODO put the overlay_layer and the text_layer into a group

                    dialog.destroy()
                    continue
                else:
                    dialog.destroy()
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL,
                                                       GLib.Error())

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AddBaloon.__gtype__, sys.argv)