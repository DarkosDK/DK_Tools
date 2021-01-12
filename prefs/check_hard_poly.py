import bpy

# from ..utility.variables import addon_name
addon_name = __name__.partition('.')[0]

class DK_Check_Hard_Poly_Preferences(bpy.types.AddonPreferences):
    bl_idname = addon_name

    hard_color: bpy.props.FloatVectorProperty(
        name='Big Polycount Color',
        description='Color of the models, which polycount more than threshold',
        size=4,
        min=0,
        max=1,
        subtype='COLOR',
        default=(1, 0, 0, 1))

    normal_color: bpy.props.FloatVectorProperty(
        name='Normal Polycount Color',
        description='Color of the models, which polycount lower than threshold',
        size=4,
        min=0,
        max=1,
        subtype='COLOR',
        default=(0, 1, 0, 1))

    def draw(self, context):
        layout = self.layout
        layout.label(text='Colors',  icon='RESTRICT_COLOR_ON')
        box = layout.box()
        row = box.row()
        row.prop(self, 'hard_color')
        row = box.row()
        row.prop(self, 'normal_color')
