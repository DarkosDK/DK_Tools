import bpy

from .circle_array import DK_OT_circle_array
from .align_to_plane import DK_OT_align_to_plane
from .subdiv_control import DK_OT_subdiv_iterations, \
                            DK_OT_subdiv_delete, \
                            DK_OT_subdiv_add, \
                            DK_OT_subdiv_on_top, \
                            DK_OT_collapse_to_subdiv, \
                            DK_OT_subdiv_low, \
                            DK_OT_subdiv_high, \
                            DK_OT_subdiv_show, \
                            DK_OT_subdiv_hide, \
                            DK_OT_collapse_to_custom_mod
from .mass_import import DK_OT_fbx_mass, DK_OT_replace_duplicate_materials
from .check_hard_poly import DK_OT_Check_Hard_Poly
from .selsim import DK_OP_Select_Similar


classes = (
    DK_OT_circle_array,
    DK_OT_align_to_plane,
    DK_OT_subdiv_iterations,
    DK_OT_subdiv_delete,
    DK_OT_subdiv_add,
    DK_OT_subdiv_on_top,
    DK_OT_collapse_to_subdiv,
    DK_OT_subdiv_low,
    DK_OT_subdiv_high,
    DK_OT_subdiv_show,
    DK_OT_subdiv_hide,
    DK_OT_collapse_to_custom_mod,
    DK_OT_fbx_mass,
    DK_OT_replace_duplicate_materials,
    DK_OT_Check_Hard_Poly,
    DK_OP_Select_Similar,
)


def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
