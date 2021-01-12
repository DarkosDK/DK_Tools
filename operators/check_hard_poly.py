import bpy
import bmesh
from math import radians
from mathutils import Quaternion, Vector


addon_name = __name__.partition('.')[0]

class DK_OT_Check_Hard_Poly(bpy.types.Operator):
    bl_idname = "dk.check_hard_poly"
    bl_label = "Check Hard Poly"
    bl_description = "Check Geometry for high polycount"
    bl_options = {'REGISTER', 'UNDO'}

    is_check: bpy.props.BoolProperty(
        name='Is Operator check',
        default=False,
    )
    polycount: bpy.props.IntProperty(
        name='Polycount',
        min=0,
        soft_max=1000000,
        default=100000,
    )
    is_select: bpy.props.BoolProperty(
        name='Is Select After Checking',
        default=False,
    )
    is_add_collection: bpy.props.BoolProperty(
        name='Add Hard Poly Objects to new Collection',
        default=False,
    )

    @ classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            # if context.object.mode == 'OBJECT':
            if context.space_data.shading.type == 'SOLID' or context.space_data.shading.type == 'WIREFRAME':
                return True
        return False

    def draw(self, context):
        layout = self.layout
        # layout.label(text='--testing--')
        if self.is_check:
            row = layout.row()
            row.label(text='Polycount:')
            row.prop(self, 'polycount', text='')
        else:
            pass

    def invoke(self, context, event):

        addon_prefs = context.preferences.addons[addon_name].preferences

        # init objects parameters
        if context.space_data.shading.type == 'SOLID':
            self.init_display_mod = context.space_data.shading.color_type
        if context.space_data.shading.type == 'WIREFRAME':
            self.init_display_mod = context.space_data.shading.wireframe_color_type
        if self.is_check:
            if context.space_data.shading.type == 'SOLID':
                context.space_data.shading.color_type = 'OBJECT'
            else:
                context.space_data.shading.wireframe_color_type = 'OBJECT'
            context.scene.init_view_mode = self.init_display_mod
            # if self.init_display_mod != 'OBJECT':
            #     context.scene.init_view_mode = self.init_display_mod
        else:
            if context.space_data.shading.type == 'SOLID':
                context.space_data.shading.color_type = context.scene.init_view_mode
            else:
                if context.scene.init_view_mode == 'MATERIAL':
                    context.space_data.shading.wireframe_color_type = 'SINGLE'
                else:
                    context.space_data.shading.wireframe_color_type = context.scene.init_view_mode

        self.hard_polycount_color = addon_prefs.hard_color
        self.normal_polycount_color = addon_prefs.normal_color
        self.arr = dict()
        self.names = []

        objects = context.scene.objects
        depsgraph = context.evaluated_depsgraph_get()

        if self.is_check:
            for obj in objects:
                if obj.type == 'MESH' and obj.visible_get():
                    obj_name = obj.name
                    bm = bmesh.new()
                    bm.from_object(obj, depsgraph)
                    polycount = len(bm.faces)
                    self.arr[obj_name] = polycount

                    # Set init colors
                    obj.init_obj_color = obj.color
        else:
            for hp_obj in context.scene.hp_objects:
                self.arr[hp_obj.name] = hp_obj.value

        return self.execute(context)

    def execute(self, context):
        context.scene.is_polycheck = self.is_check

        # Turn on checking
        if self.is_check:
            context.scene.hp_objects.clear()
            for obj in context.scene.objects:
                if obj.type == 'MESH' and obj.visible_get():
                    if self.arr[obj.name] > self.polycount:
                        obj.init_obj_color = obj.color
                        obj.color = self.hard_polycount_color
                        self.names.append(obj.name)
                        obj.is_hp = True
                        my_item = context.scene.hp_objects.add()
                        my_item.name = obj.name
                        my_item.value = self.arr[obj.name]
                    else:
                        obj.init_obj_color = obj.color
                        obj.color = self.normal_polycount_color
                        obj.is_hp = False

        # Turn off checking
        else:
            for obj in context.scene.objects:
                obj.color = list(obj.init_obj_color)

            sort_hp_list = sorted([key for key in self.arr.keys()], reverse=True, key=lambda ob_name: self.arr[ob_name]) 
            if self.is_select:
                if len(sort_hp_list) != 0:
                    bpy.ops.object.select_all(action='DESELECT')
                    for name_obj in sort_hp_list:
                        obj = context.scene.objects[name_obj]
                        if sort_hp_list.index(name_obj) == 0:
                            context.view_layer.objects.active = obj
                        obj.select_set(True)
            elif self.is_add_collection:
                if len(sort_hp_list) != 0:
                    # Create new collection
                    new_col = bpy.data.collections.new('High Polycount Objects')
                    bpy.context.scene.collection.children.link(new_col)

                    for name_obj in sort_hp_list:
                        obj = context.scene.objects[name_obj]

                        # Init collections - when HP objects location
                        init_col = obj.users_collection

                        # Put to new collection
                        new_col.objects.link(obj)

                        # Delete from init collection
                        for col in init_col:
                            col.objects.unlink(obj)


        return {'FINISHED'}