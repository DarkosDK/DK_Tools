import bpy

from .check_hard_poly import DK_Check_Hard_Poly_Preferences

classes = (
    DK_Check_Hard_Poly_Preferences,
)


def register_prefs():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_prefs():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
