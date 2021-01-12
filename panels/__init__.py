import bpy

from .circle_array import VIEW3D_PT_DK_Circle_Array
from .align_to_plane import VIEW3D_PT_DK_Align_to_Plane
from .subdiv_control import VIEW3D_PT_DK_subdivide_control
from .mass_import import VIEW3D_PT_DK_mass_fbx_import
from .check_hard_poly import VIEW3D_PT_DK_Check_Hard_Poly
from .selsim import VIEW3D_PT_DK_Select_Similar


classes = (
    VIEW3D_PT_DK_Circle_Array,
    VIEW3D_PT_DK_Align_to_Plane,
    VIEW3D_PT_DK_subdivide_control,
    VIEW3D_PT_DK_mass_fbx_import,
    VIEW3D_PT_DK_Check_Hard_Poly,
    VIEW3D_PT_DK_Select_Similar,
)


def register_panels():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_panels():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
