#! /usr/bin/env python2.6
'''
message_element.py
A patch element corresponding to a clickable message

Copyright (c) 2010 Bill Gribble <grib@billgribble.com>
'''

from gi.repository import Clutter as clutter 
import math 
from patch_element import PatchElement
from mfp import MFPGUI
from .modes.label_edit import LabelEditMode
from mfp import log 

class MessageElement (PatchElement):
	element_type = "message"
	PORT_TWEAK = 5 
	def __init__(self, window, x, y):
		PatchElement.__init__(self, window, x, y)

		self.message_text = None 

		# create elements
		self.texture = clutter.CairoTexture.new(35,25)
		self.label = clutter.Text()

		self.texture.set_size(35, 25)
		self.texture.connect("draw", self.draw_cb)

		self.set_reactive(True)
		self.add_actor(self.texture)
		self.add_actor(self.label)

		self.texture.invalidate()

		# configure label
		self.label.set_position(4, 1)
		self.label.set_color(window.color_unselected) 
		self.label.connect('text-changed', self.text_changed_cb)

		# click handler 
		self.connect('button-press-event', self.button_press_cb)
		
		self.move(x, y)

		# request update when value changes
		self.update_required = True

	def draw_cb(self, texture, ct):
		w = self.texture.get_property('surface_width')-2
		h = self.texture.get_property('surface_height')-2
		c = None
		if self.selected: 
			c = self.stage.color_selected
		else:
			c = self.stage.color_unselected
		ct.set_source_rgb(c.red, c.green, c.blue)

		ct.translate(0.5, 0.5)
		ct.move_to(1,1)
		ct.line_to(1, h)
		ct.line_to(w, h)
		ct.curve_to(w-8, h-8, w-8, 8, w, 1)
		ct.line_to(1,1)
		ct.close_path()
		ct.stroke()

	def button_press_cb(self, *args):
		MFPGUI().mfp.send_bang(self.obj_id, 0) 

	def label_edit_start(self):
		pass

	def label_edit_finish(self, *args):
		self.message_text = self.label.get_text()

		self.create(self.element_type, self.message_text)
		if self.obj_id is None:
			log.debug("MessageElement: could not create message obj for '%s'" 
						% self.message_text)
		else:
			self.send_params()
			self.draw_ports()

	def text_changed_cb(self, *args):
		lwidth = self.label.get_property('width') 
		bwidth = self.texture.get_property('surface_width')
	
		new_w = None 
		if (lwidth > (bwidth - 20)):
			new_w = lwidth + 20
		elif (bwidth > 35) and (lwidth < (bwidth - 20)):
			new_w = max(35, lwidth + 20)

		if new_w is not None:
			self.set_size(new_w, self.texture.get_height())
			self.texture.set_size(new_w, self.texture.get_height())
			self.texture.set_surface_size(int(new_w), self.texture.get_property('surface_height'))
			self.texture.invalidate()	

	def move(self, x, y):
		self.position_x = x
		self.position_y = y
		self.set_position(x, y)

		for c in self.connections_out:
			c.draw()
		
		for c in self.connections_in:
			c.draw()

	def configure(self, params):
		if params.get('value') is not None:
			self.label.set_text(repr(params.get('value')))
		elif self.obj_args is not None:
			self.label.set_text(self.obj_args)
		PatchElement.configure(self, params)	

	def port_position(self, port_dir, port_num):
		# tweak the right input port display to be left of the "kick" 
		if port_dir == PatchElement.PORT_IN and port_num == 1:
			default = PatchElement.port_position(self, port_dir, port_num)
			return (default[0] - self.PORT_TWEAK, default[1])
		else:
			return PatchElement.port_position(self, port_dir, port_num)

	def select(self):
		self.selected = True 
		self.texture.invalidate()

	def unselect(self):
		self.selected = False 
		self.texture.invalidate()

	def delete(self):
		for c in self.connections_out+self.connections_in:
			c.delete()
		PatchElement.delete(self)

	def make_edit_mode(self):
		return LabelEditMode(self.stage, self, self.label)



