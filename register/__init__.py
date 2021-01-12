def register_addon():

    # Props
    from ..props import register_properties
    register_properties()

    # Prefs
    from ..prefs import register_prefs
    register_prefs()

    # Operators
    from ..operators import register_operators
    register_operators()

    # Panels
    from ..panels import register_panels
    register_panels()


def unregister_addon():

    # Props
    from ..props import unregister_properties
    unregister_properties()

    # Prefs
    from ..prefs import unregister_prefs
    unregister_prefs()

    # Panels
    from ..panels import unregister_panels
    unregister_panels()

    # Operators
    from ..operators import unregister_operators
    unregister_operators()
