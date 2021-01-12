bl_info = {
    "name": "",
    "author": "DarkosDK",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "category": "3D View",
    "location": "View3D",
    "description": "Convenient tools for work",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}


def register():
    from .register import register_addon
    register_addon()


def unregister():
    from .register import unregister_addon
    unregister_addon()
