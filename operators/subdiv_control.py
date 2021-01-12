import bpy
import bmesh

from math import radians
from mathutils import Quaternion, Vector


class DK_OT_subdiv_iterations(bpy.types.Operator):
    """Set iteration level to selections objects"""
    bl_idname = "dk.set_subdiv_iters"
    bl_label = "Set Sub Iterations"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if objects is not None and len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        name = mod.name
                        obj.modifiers[name].render_levels = context.scene.iters
                        obj.modifiers[name].levels = context.scene.iters

        return {'FINISHED'}


class DK_OT_subdiv_delete(bpy.types.Operator):
    """Delete Subdivide modifiers from all selected objects"""
    bl_idname = "dk.del_subdiv"
    bl_label = "Delete Subdivide"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        obj.modifiers.remove(mod)
        return {'FINISHED'}


class DK_OT_subdiv_add(bpy.types.Operator):
    """Add Subdivide modifiers from all selected objects"""
    bl_idname = "dk.add_subdiv"
    bl_label = "Add Subdivide"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            isSubd = False
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        isSubd = True
            if not isSubd:
                s = obj.modifiers.new(name='Subdivision', type='SUBSURF')
                s.levels = context.scene.iters
                s.render_levels = context.scene.iters
        return {'FINISHED'}


class DK_OT_subdiv_on_top(bpy.types.Operator):
    """Move Subdivide modifier on top of the stack in all selected objects"""
    bl_idname = "dk.top_subdiv"
    bl_label = "Add Subdivide"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        active_obj = bpy.context.active_object
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                mod_count = len(obj.modifiers)
                mod_subd = None
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        mod_subd = mod
                if mod_subd is not None:
                    context.view_layer.objects.active = obj
                    mod_name = mod_subd.name
                    all_mods = [m.name for m in obj.modifiers]
                    mod_subd_pos = all_mods.index(mod_name)
                    dive = mod_count - mod_subd_pos
                    for i in range(0, dive):
                        bpy.ops.object.modifier_move_down(modifier=mod_name)
        context.view_layer.objects.active = active_obj
        return {'FINISHED'}


class DK_OT_collapse_to_subdiv(bpy.types.Operator):
    """Collapse all modifiers before Subdivision in all selected objects"""
    bl_idname = "dk.collapse_to_subdiv"
    bl_label = "Collapse"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        active_obj = bpy.context.active_object
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                mod_count = len(obj.modifiers)
                mod_subd = None
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        mod_subd = mod
                if mod_subd is not None:
                    context.view_layer.objects.active = obj
                    mod_name = mod_subd.name
                    all_mods = [m.name for m in obj.modifiers]
                    mod_subd_pos = all_mods.index(mod_name)
                    mods_to_collapse = [m.name for m in obj.modifiers if
                                        all_mods.index(m.name) < mod_subd_pos]
                    if len(mods_to_collapse) != 0:
                        for i in mods_to_collapse:
                            bpy.ops.object.modifier_apply(modifier=i)
                    '''
                    mod_subd_pos = all_mods.index(mod_name)
                    dive = mod_count - mod_subd_pos
                    for i in range(0, dive):
                        bpy.ops.object.modifier_move_down(modifier=mod_name)
                    context.view_layer.objects.active = active_obj
                    '''
        context.view_layer.objects.active = active_obj
        return {'FINISHED'}


class DK_OT_subdiv_low(bpy.types.Operator):
    """Decrease Subdivide level on all selected objects"""
    bl_idname = "dk.low_subdiv"
    bl_label = "Decrease Subdivide Level"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        name = mod.name
                        iters_r = obj.modifiers[name].render_levels
                        iters = obj.modifiers[name].levels
                        obj.modifiers[name].render_levels = clamp_to_zero(iters_r - 1)
                        obj.modifiers[name].levels = clamp_to_zero(iters - 1)
        return {'FINISHED'}


class DK_OT_subdiv_high(bpy.types.Operator):
    """Increase Subdivide level on all selected objects"""
    bl_idname = "dk.high_subdiv"
    bl_label = "Increase Subdivide Level"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        name = mod.name
                        iters_r = obj.modifiers[name].render_levels
                        iters = obj.modifiers[name].levels
                        obj.modifiers[name].render_levels = iters_r + 1
                        obj.modifiers[name].levels = iters + 1
        return {'FINISHED'}


class DK_OT_subdiv_show(bpy.types.Operator):
    """Show Subdivide in viewport on all selected objects"""
    bl_idname = "dk.show_subdiv"
    bl_label = "Show Subdivide in viewport"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        name = mod.name
                        obj.modifiers[name].show_viewport = True
        return {'FINISHED'}


class DK_OT_subdiv_hide(bpy.types.Operator):
    """Hide Subdivide in viewport on all selected objects"""
    bl_idname = "dk.hide_subdiv"
    bl_label = "Hide Subdivide in viewport"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def execute(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        name = mod.name
                        obj.modifiers[name].show_viewport = False
        return {'FINISHED'}


class DK_OT_collapse_to_custom_mod(bpy.types.Operator):
    """Collapse all modifiers to selected modifier in all selected objects"""
    bl_idname = "dk.collapse_to_mod"
    bl_label = "Collapse to modifier"
    bl_options = {'REGISTER', 'UNDO'}

    def item_callback(self, context):
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        modifiers_to_collapse = []
        for obj in objects:
            if len(obj.modifiers) != 0:
                for mod in obj.modifiers:
                    m = (mod.type, mod.type, mod.type)
                    modifiers_to_collapse.append(m)
        modifiers_to_collapse = list(set(modifiers_to_collapse))
        return modifiers_to_collapse

    collapse_to_mod: bpy.props.EnumProperty(
        items=item_callback,
        name="",
        default=None,
    )

    is_apply: bpy.props.BoolProperty(
        default=False,
        name='Apply',
    )

    is_include: bpy.props.BoolProperty(
        default=False,
        name='Include this modifier'
    )

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            objects = None
            if not context.scene.is_on_selection:
                objects = context.scene.objects
            else:
                objects = context.selected_objects
            if len(objects) != 0:
                return True

    def draw(self, context):
        layout = self.layout
        row1 = layout.row(align=True)
        row1.prop(self, 'collapse_to_mod')
        row1.prop(self, 'is_include')
        row2 = layout.row(align=True)
        row2.prop(self, 'is_apply')
        if self.is_apply:
            row1.enabled = False
        else:
            row1.enabled = True

    def invoke(self, context, event):
        self.is_apply = False
        return self.execute(context)

    def execute(self, context):
        active_obj = bpy.context.active_object
        objects = None
        if not context.scene.is_on_selection:
            objects = context.scene.objects
        else:
            objects = context.selected_objects
        if self.is_apply:
            for obj in objects:
                if len(obj.modifiers) != 0:
                    mod_count = len(obj.modifiers)
                    mod_subd = None
                    for mod in obj.modifiers:
                        if mod.type == self.collapse_to_mod:
                            mod_subd = mod
                    if mod_subd is not None:
                        context.view_layer.objects.active = obj
                        mod_name = mod_subd.name
                        all_mods = [m.name for m in obj.modifiers]
                        mod_subd_pos = all_mods.index(mod_name)
                        if self.is_include:
                            mod_subd_pos += 1
                        mods_to_collapse = [m.name for m in obj.modifiers if all_mods.index(m.name) < mod_subd_pos]
                        if len(mods_to_collapse) != 0:
                            for i in mods_to_collapse:
                                try:
                                    bpy.ops.object.modifier_apply(modifier=i)
                                except Exception:
                                    print("Multy-user data")
        context.view_layer.objects.active = active_obj
        return {'FINISHED'}
