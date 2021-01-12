import bpy


class VIEW3D_PT_DK_subdivide_control(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DK"
    bl_label = "Subdivision Control"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.prop(context.scene, 'is_on_selection')
        split = box.split(factor=0.25)
        col_1 = split.column()
        col_2 = split.column()
        col_1.prop(context.scene, 'iters')
        col_2.operator('dk.set_subdiv_iters', text='Set Iterations')
        row = box.row()
        row.operator('dk.del_subdiv', text='Delete')
        row.operator('dk.add_subdiv', text='Add')
        row = box.row()
        row.operator('dk.top_subdiv', text='On Top')
        row = box.row()
        row.operator('dk.collapse_to_subdiv', text='Collapse to Subdivide')
        row = box.row()
        row.operator('dk.collapse_to_mod', text='Collapse to:')
        split = box.split(factor=0.3)
        col_1 = split.column()
        col_2 = split.row()
        col_1.label(text="Iterations:")
        col_2.operator('dk.low_subdiv', text='Low', icon='REMOVE')
        col_2.operator('dk.high_subdiv', text='High', icon='ADD')
        split = box.split(factor=0.3)
        col_1 = split.column()
        col_2 = split.row()
        col_1.label(text="Modifier:")
        col_2.operator('dk.hide_subdiv', text='Hide', icon='HIDE_ON')
        col_2.operator('dk.show_subdiv', text='Show', icon='HIDE_OFF')
