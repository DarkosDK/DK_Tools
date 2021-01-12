import bpy

from math import radians
from mathutils import Quaternion, Vector

from ..utility.variables import axis_items, rotation_center_options


class DK_OT_circle_array(bpy.types.Operator):
    """More convenient circle array"""
    bl_idname = "dk.circle_array"
    bl_label = "Circle Array"
    bl_options = {'REGISTER', 'UNDO'}
    obj_clear_pos = Vector((0, 0, 0))

    # operator properties

    axis: bpy.props.EnumProperty(
        items=axis_items,
        name="",
    )
    rotation_center: bpy.props.EnumProperty(
        items=rotation_center_options,
        name="",
    )
    count: bpy.props.IntProperty(
        name='Count',
        default=2,
        min=2,
        soft_max=10
    )
    angle: bpy.props.FloatProperty(
        name='Angle',
        default=radians(360.0),
        min=0.0,
        max=radians(360.0),
        subtype='ANGLE'
    )
    use_bias: bpy.props.BoolProperty(
        name='Use Bias',
        default=False
    )
    bias: bpy.props.FloatProperty(
        name='',
        default=1.0
    )

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            ob = context.active_object
            if context.scene.rotation_center == 'Object' and \
                    not context.scene.chosen_object:
                return False
            elif ob is not None and ob.mode == 'OBJECT':
                return True

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row_2 = layout.row(align=True)
        row_2.label(text='Axis')
        row_2.prop(self, 'axis')
        row_3 = layout.row(align=True)
        row_3.prop(self, 'count')
        row_3.prop(self, 'angle')
        row_4 = layout.row(align=True)
        row_4.prop(self, 'use_bias')
        row_5 = layout.row(align=True)
        row_5.label(text='Bias')
        row_5.prop(self, 'bias')
        if not self.use_bias:
            row_5.enabled = False
        if self.rotation_center == 'Pivot':
            self.use_bias = False
            row_4.enabled = False

    def invoke(self, context, event):
        self.rotation_center = context.scene.rotation_center
        self.obj_clear_pos = context.active_object.location
        return self.execute(context)

    def execute(self, context):
        print(context.scene.chosen_object)
        obj = context.active_object
        cursor = context.scene.cursor.location  # Vector? cursor location

        rot_axis = Vector((1.0, 0.0, 0.0))
        if self.axis == 'Y':
            rot_axis = Vector((0.0, 1.0, 0.0))
        elif self.axis == 'Z':
            rot_axis = Vector((0.0, 0.0, 1.0))

        if context.scene.rotation_center != 'Object':
            obj_init_rot_mod = obj.rotation_mode
            obj.rotation_mode = 'QUATERNION'
            obj_rot_quaternion = obj.rotation_quaternion
            rot_axis.rotate(obj_rot_quaternion)
            obj.rotation_mode = obj_init_rot_mod

        rot_center = obj.location
        if self.rotation_center == '3D Cursor':
            rot_center = cursor
        elif self.rotation_center == 'Object' and context.scene.chosen_object:
            rot_center_object = context.scene.chosen_object
            rot_center = rot_center_object.location
            init_rot_mod = rot_center_object.rotation_mode
            rot_center_object.rotation_mode = 'QUATERNION'
            rot_center_quaternion = rot_center_object.rotation_quaternion
            rot_axis.rotate(rot_center_quaternion)
            rot_center_object.rotation_mode = init_rot_mod

        rot_angle_whole = self.angle

        obj_col = obj.users_collection[0]
        copy_count = self.count
        for i in range(1, copy_count):
            rot_angle = (rot_angle_whole / (copy_count - 1)) * i
            if round(self.angle, 5) == round(radians(360), 5):
                rot_angle = (rot_angle_whole / copy_count) * i
            copy_obj = obj.copy()
            obj_col.objects.link(copy_obj)

            rot_quaternion = Quaternion(rot_axis, rot_angle)

            vector_to_rot = copy_obj.location - rot_center
            if self.use_bias:
                # vector_to_rot *= self.bias
                vector_to_rot_project = vector_to_rot.project(rot_axis)
                delta = vector_to_rot - vector_to_rot_project
                delta *= self.bias
                vector_to_rot = vector_to_rot_project + delta

            vector_to_rot.rotate(rot_quaternion)
            copy_obj.location = vector_to_rot + rot_center

            obj_init_rot_mod = copy_obj.rotation_mode
            copy_obj.rotation_mode = 'QUATERNION'
            copy_obj.rotation_quaternion = rot_quaternion @ \
                copy_obj.rotation_quaternion
            copy_obj.rotation_mode = obj_init_rot_mod
        if self.use_bias:
            vector_obj = obj.location - rot_center
            vector_obj_project = vector_obj.project(rot_axis)
            delta = vector_obj - vector_obj_project
            # vector_obj *= self.bias
            delta *= self.bias
            vector_obj = vector_obj_project + delta
            # obj.location = rot_center + vector_obj
            obj.location = rot_center + vector_obj
        else:
            obj.location = self.obj_clear_pos
            print("test_not_bias")

        return {'FINISHED'}
