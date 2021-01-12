import bpy


class VIEW3D_PT_DK_Circle_Array(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DK"
    bl_label = "Array"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Rotation Center")
        row.prop(context.scene, 'rotation_center')
        row_2 = layout.row(align=True)
        row_2.prop_search(
            context.scene,
            "chosen_object",
            context.scene,
            "objects")
        row_2.enabled = False
        if bpy.context.scene.rotation_center == 'Object':
            row_2.enabled = True
        col = layout.column(align=True)
        col.operator('dk.circle_array', icon='PROP_OFF')
