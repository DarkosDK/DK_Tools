import bpy


class VIEW3D_PT_DK_mass_fbx_import(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DK"
    bl_label = "Mass FBX Import"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene, 'mass_import_fbx_path')
        col.prop(context.scene, 'use_fbx_subsurf')
        col.operator('dk.fbx_mass')
        col = layout.column(align=True)
        col.operator('dk.replace_duplicate_materials', text='Fix Materials')
