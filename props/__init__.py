import bpy

from ..utility.functions import update_func
from ..utility.variables import rotation_center_options, align_planes
from ..utility.variables import axis_items


class DK_Scene_HP_Models_List(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Object Name', default='Unknown')
    value: bpy.props.IntProperty(name='Object Polycount', default=0)


classes = (
    DK_Scene_HP_Models_List,
)


def register_properties():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.hp_objects = bpy.props.CollectionProperty(
        type=DK_Scene_HP_Models_List)

    bpy.types.Scene.is_polycheck = bpy.props.BoolProperty(
        name='Is Polycount Check On',
        default=False,
    )

    bpy.types.Scene.init_view_mode = bpy.props.StringProperty(
        name='Init View Mode',
        default='MATERIAL',
    )

    bpy.types.Object.init_obj_color = bpy.props.FloatVectorProperty(
        name='Init Color',
        size=4,
        subtype='COLOR',
    )
    bpy.types.Object.is_hp = bpy.props.BoolProperty(
        name='Is High Polycount Object',
        default=False,
    )

    bpy.types.Scene.mass_import_fbx_path = bpy.props.StringProperty(
        name='FBX Folder',
        subtype='DIR_PATH',
    )
    bpy.types.Scene.use_fbx_subsurf = bpy.props.BoolProperty(
        name='Use Subsurf',
        default=False,
    )
    bpy.types.Scene.chosen_object = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Center',
        update=update_func
    )
    bpy.types.Scene.rotation_center = bpy.props.EnumProperty(
        items=rotation_center_options,
        name='',
        update=update_func
    )
    bpy.types.Scene.align_direction = bpy.props.EnumProperty(
        items=align_planes,
        name='text',
        default='- Z'
    )
    bpy.types.Scene.iters = bpy.props.IntProperty(
        name='',
        default=1,
        min=0,
    )
    bpy.types.Scene.is_on_selection = bpy.props.BoolProperty(
        name='Only on Selection',
        default=False,
    )


def unregister_properties():

    del bpy.types.Scene.hp_objects

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.is_on_selection
    del bpy.types.Scene.iters
    del bpy.types.Scene.align_direction
    del bpy.types.Scene.rotation_center
    del bpy.types.Scene.chosen_object
    del bpy.types.Scene.use_fbx_subsurf
    del bpy.types.Scene.mass_import_fbx_path
    del bpy.types.Object.is_hp
    del bpy.types.Object.init_obj_color
    del bpy.types.Scene.init_view_mode
    del bpy.types.Scene.is_polycheck
