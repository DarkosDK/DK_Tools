import bpy
import pathlib
import os


class DK_OT_fbx_mass(bpy.types.Operator):
    bl_idname = 'dk.fbx_mass'
    bl_label = "Mass-import FBX files"

    def execute(self, context):
        abspath = bpy.path.abspath(context.scene.mass_import_fbx_path)
        import_path = pathlib.Path(abspath)
        for import_fpath in import_path.glob('*.fbx'):

            # Define Collection name
            name_with_expansion = os.path.basename(import_fpath)
            collection_name = name_with_expansion.rpartition('.')[0]

            # Create collection
            new_col = None
            if bpy.context.view_layer.layer_collection.children.find(collection_name) != -1:
                new_col = bpy.context.view_layer.layer_collection.children[collection_name]
            else:
                new_col = bpy.data.collections.new(collection_name)
                bpy.context.scene.collection.children.link(new_col)

            # Set active collection
            layer_collection = bpy.context.view_layer.layer_collection.children[collection_name]
            bpy.context.view_layer.active_layer_collection = layer_collection

            # Import fbx
            bpy.ops.import_scene.fbx(filepath=str(import_fpath),
                                     use_custom_normals=False,
                                     use_subsurf=context.scene.use_fbx_subsurf)

        # Close collections in outliner

        override = bpy.context.copy()
        for area in bpy.context.screen.areas:
            if area.type == 'OUTLINER':
                override['area'] = area
                bpy.ops.wm.redraw_timer(type='DRAW_WIN', iterations=1)
                bpy.ops.outliner.show_one_level(override, open=False)
                area.tag_redraw()

        return {'FINISHED'}


class DK_OT_replace_duplicate_materials(bpy.types.Operator):
    """Replace duplicated materials after import"""
    bl_idname = "dk.replace_duplicate_materials"
    bl_label = "Replace Duplicate Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mats = bpy.data.materials

        for obj in bpy.context.scene.objects:
            for slot in obj.material_slots:
                part = slot.name.rpartition('.')
                mat = mats.get(part[0])
                if part[2].isnumeric() and mat is not None:
                    slot.material = mat

        return {'FINISHED'}
