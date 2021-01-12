import bpy


class VIEW3D_PT_DK_Select_Similar(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DK"
    bl_label = "Select Similar"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator('dk.selectsim', text='Select Similar by Topology')
