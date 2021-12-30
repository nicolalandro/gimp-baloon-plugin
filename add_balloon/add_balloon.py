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
# gettext.bind_textdomain_codeset(textdomain, 'UTF-8')
gettext.textdomain(textdomain)
_ = gettext.gettext
def N_(message): return message

class AddBalloon(Gimp.PlugIn):
    def do_query_procedures(self):
        self.set_translation_domain(textdomain,
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return [ "plug-in-add-balloon" ]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                       Gimp.PDBProcType.PLUGIN,
                                       self.run, None)

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask (Gimp.ProcedureSensitivityMask.DRAWABLE)

        procedure.set_menu_label(N_("Add Balloon..."))
        procedure.set_icon_name(GimpUi.ICON_GEGL)
        procedure.add_menu_path('<Image>/Select')

        procedure.set_documentation(N_("Add a text for balloon"),
                                    N_("Add text and a layer with white inside the selection"),
                                    name)
        procedure.set_attribution("Z-UO", "Z-UO", "2022")

        return procedure

    def run(self, procedure, run_mode, image, n_drawables, drawables, args, run_data):
        if n_drawables != 1:
            msg = _(f"Procedure '{procedure.get_name()}' only works with one drawable.")
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)
        else:
            drawable = drawables[0]

        # check if selection exist
        selection = image.get_selection()
        flag, non_empty, x1, y1, x2, y2 = selection.bounds(image)
        if not non_empty:
            msg = _(f"The selection is empty, create a selection box and precede with the use of this plugin.")
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)

        if run_mode == Gimp.RunMode.INTERACTIVE:
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gdk

            GimpUi.init("add_balloon.py")

            dialog = GimpUi.Dialog(use_header_bar=True,
                                   title=_("Add Balloon)"),
                                   role="add_balloon-Python3")
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

            # Improve UI
            font_chooser = Gtk.FontChooserWidget()
            box.pack_start(font_chooser, False, False, 1)
            font_chooser.show()

            # TODO add spinner for waiting

            while (True):
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    # TODO enable spinner and lock all other values

                    # layer position
                    position = Gimp.get_pdb().run_procedure('gimp-image-get-item-position',
                                 [image,
                                  drawable]).index(1)
                    # Create group
                    layer_group = Gimp.get_pdb().run_procedure('gimp-layer-group-new',
                                 [image]).index(1)
                    image.insert_layer(layer_group,None,position)

                    # add new trasparent layer
                    overlay_layer = Gimp.Layer.new(
                        image, 'hide_background',
                        drawable.get_width(), drawable.get_height(),
                        Gimp.ImageType.RGBA_IMAGE, 100.0,
                        Gimp.LayerMode.NORMAL
                    )
                    image.insert_layer(overlay_layer,layer_group,position)
                    overlay_layer.fill(Gimp.FillType.TRANSPARENT)

                    # add white fill the selection
                    Gimp.get_pdb().run_procedure('gimp-drawable-edit-fill',
                                 [overlay_layer,
                                  Gimp.FillType.WHITE])

                    # add text layer
                    buffer = text_content.get_buffer()
                    text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)

                    font_str = font_chooser.get_font()
                    font_size = float(font_str.split(' ')[-1])
                    font_name = ' '.join(font_str.split(' ')[0:-2])

                    text_layer = Gimp.get_pdb().run_procedure('gimp-text-layer-new',
                                 [image, text, font_name, font_size, 3
                                  ]).index(1)
                    image.insert_layer(text_layer,layer_group,position - 1)

                    # center text layer
                    Gimp.get_pdb().run_procedure('gimp-text-layer-set-justification',
                                 [text_layer, 2])
                    cx = (x1 + x2)/2 - text_layer.get_width()/2
                    cy = (y1 + y2)/2 - text_layer.get_height()/2
                    Gimp.get_pdb().run_procedure('gimp-item-transform-translate',
                                 [text_layer, cx, cy])

                    # set selected layer
                    image.set_selected_layers([layer_group])


                    dialog.destroy()
                    break
                else:
                    dialog.destroy()
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL,
                                                       GLib.Error())

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AddBalloon.__gtype__, sys.argv)
