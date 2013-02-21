#! /usr/bin/env python
'''
patch_funcs.py
Helper methods for patch window input modes

Copyright (c) 2012 Bill Gribble <grib@billgribble.com>
'''
from ..utils import extends
from .patch_window import PatchWindow
from .patch_element import PatchElement
from .connection_element import ConnectionElement
from .modes.select_mru import SelectMRUMode
from ..gui_slave import MFPGUI

@extends(PatchWindow)
def patch_select_prev(self): 
    if not self.selected_patch:
        self.layer_select(self.patches[0].layers[0])
    else:
        pnum = self.patches.index(self.selected_patch)
        pnum -= 1
        self.layer_select(self.patches[pnum].layers[0])

@extends(PatchWindow)
def patch_select_next(self): 
    if not self.selected_patch:
        self.layer_select(self.patches[0].layers[0])
    else:
        pnum = self.patches.index(self.selected_patch)
        pnum = (pnum + 1) % len(self.patches)
        self.layer_select(self.patches[pnum].layers[0])

@extends(PatchWindow)
def patch_close(self):
    if len(self.patches) > 1:
        p = self.selected_patch
        self.patch_select_next() 
        self.patches.remove(p)
        p.delete()
    else: 
        self.quit()

@extends(PatchWindow)
def patch_new(self):
    MFPGUI().mfp.open_file(None)

@extends(PatchWindow)
def _select(self, obj): 
    if obj is None or not isinstance(obj, PatchElement):
        return 

    self.selected = obj
    obj.select()
    obj.begin_control()

    # FIXME hook
    self.emit_signal("select", obj)


@extends(PatchWindow)
def select(self, obj):
    if self.selected is obj: 
        return True 

    if self.selected is not None:
        self._unselect(self.selected)

    self._select(obj)
    self.object_view.select(obj)
    return True


@extends(PatchWindow)
def _unselect(self, obj):
    if obj is None:
        return 
    if isinstance(obj, PatchElement):
        if obj.edit_mode:
            obj.end_edit()
        obj.end_control()
        obj.unselect()
    self.selected = None

    self.emit_signal("unselect", obj)

@extends(PatchWindow)
def unselect(self, obj):
    if self.selected is obj and obj is not None:
        self._unselect(obj)
        self.object_view.select(None)
    return True


@extends(PatchWindow)
def unselect_all(self):
    if self.selected:
        self.selected.end_control()
        self._unselect(self.selected)
        self.object_view.select(None)
    return True


@extends(PatchWindow)
def select_next(self):
    if len(self.selected_layer.objects) == 0:
        return False

    if (self.selected is None or self.selected not in self.selected_layer.objects):
        start = 0
    else:
        current = self.selected_layer.objects.index(self.selected)
        start = (current + 1) % len(self.selected_layer.objects)
    candidate = start

    for count in range(len(self.selected_layer.objects)):
        if not isinstance(self.selected_layer.objects[candidate], ConnectionElement):
            self.select(self.selected_layer.objects[candidate])
            return True
        candidate = (candidate + 1) % len(self.selected_layer.objects)
    return False


@extends(PatchWindow)
def select_prev(self):
    if len(self.selected_layer.objects) == 0:
        return False

    if (self.selected is None or self.selected not in self.selected_layer.objects):
        candidate = -1
    else:
        candidate = self.selected_layer.objects.index(self.selected) - 1

    while candidate > -len(self.selected_layer.objects):
        if not isinstance(self.selected_layer.objects[candidate], ConnectionElement):
            self.select(self.selected_layer.objects[candidate])
            return True
        candidate -= 1

    return False


@extends(PatchWindow)
def select_mru(self):
    self.input_mgr.enable_minor_mode(SelectMRUMode(self))
    return True


@extends(PatchWindow)
def move_selected(self, dx, dy):
    if self.selected is None or isinstance(self.selected, ConnectionElement):
        return

    self.selected.move(max(0, self.selected.position_x + dx * self.zoom),
                       max(0, self.selected.position_y + dy * self.zoom))
    if self.selected.obj_id is not None:
        self.selected.send_params()
    return True


@extends(PatchWindow)
def delete_selected(self):
    if self.selected is None:
        return
    o = self.selected
    o.delete()
    return True


@extends(PatchWindow)
def edit_selected(self):
    if self.selected is None:
        return True
    self.selected.begin_edit()
    return True


@extends(PatchWindow)
def rezoom(self):
    w, h = self.group.get_size()
    self.group.set_scale_full(self.zoom, self.zoom, w / 2.0, h / 2.0)
    self.group.set_position(self.view_x, self.view_y)


@extends(PatchWindow)
def reset_zoom(self):
    self.zoom = 1.0
    self.view_x = 0
    self.view_y = 0
    self.rezoom()
    return True


@extends(PatchWindow)
def zoom_out(self, ratio):
    if self.zoom >= 0.1:
        self.zoom *= ratio
        self.rezoom()
    return True


@extends(PatchWindow)
def zoom_in(self, ratio):
    if self.zoom < 20:
        self.zoom *= ratio
        self.rezoom()
    return True


@extends(PatchWindow)
def move_view(self, dx, dy):
    self.view_x += dx
    self.view_y += dy
    self.rezoom()
    return True