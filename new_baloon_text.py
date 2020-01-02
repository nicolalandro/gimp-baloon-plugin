#! /usr/bin/env python2
from gimpfu import *
import math

# for the text use https://gimplearn.net/viewtopic.php?f=3&t=2146
## Run verbose
# /usr/bin/flatpak run --branch=stable --arch=x86_64 --command=gimp-2.10 --file-forwarding org.gimp.GIMP --verbose
## dev test
# from gimpfu import *
# img=gimp.image_list()[0]
# layer=img.active_layer 

def _translate_layer_at_seclection_center(layer, x1,y1,x2,y2):
	cx = (x1 + x2)/2
	cy = (y1 + y2)/2
	pdb.gimp_item_transform_translate(layer, cx, cy)



def python_new_baloon_text(img, layer):
    non_empty,x1,y1,x2,y2 = pdb.gimp_selection_bounds(img)
    if not non_empty:
		pdb.gimp_message("Must have an active selection")
    else:
    	# create colored baloon
		box = pdb.gimp_layer_new(img, img.width,img.height, RGBA_IMAGE, layer.name + "_baloon", 100, NORMAL_MODE)
		pdb.gimp_image_insert_layer(img, box, None, -1)
		pdb.gimp_edit_fill(box, 1)
		# create text
		text_layer = pdb.gimp_text_layer_new(img, 'Text', 1, 0.1, 1)
		pdb.gimp_image_insert_layer(img, text_layer, None, -1)
		_translate_layer_at_seclection_center(text_layer,x1,y1,x2,y2)

	
register(
		"python_new_baloon_text",
		"Add Baloon with text",
		"Add a layer with white baloon and selected text content",
		"Nicola Landro",
		"Nicola Landro",
		"2020",
		"<Image>/Select/Add Baloon...",
		"*",
		[],
		[],
		python_new_baloon_text)
		
main()
