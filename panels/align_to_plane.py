import bpy


class VIEW3D_PT_DK_Align_to_Plane(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DK"
    bl_label = "Align to Plane"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, 'align_direction', expand=True)
        layout.operator('dk.align_to_plane', text='Align')
