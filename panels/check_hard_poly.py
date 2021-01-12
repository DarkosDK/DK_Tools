import bpy


class VIEW3D_PT_DK_Check_Hard_Poly(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DK"
    bl_label = "Check Polycount"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        if not context.scene.is_polycheck:
            prop = col.operator('dk.check_hard_poly',
                                text='Check Polycount')
            prop.is_check = True
            prop.is_select = False
            prop.is_add_collection = False
            layout.label(text='Presets')

            row = layout.row(align=True)
            preset_01 = row.operator('dk.check_hard_poly',
                                     text='500')
            preset_01.is_check = True
            preset_01.is_select = False
            preset_01.is_add_collection = False
            preset_01.polycount = 500

            preset_02 = row.operator('dk.check_hard_poly',
                                     text='1K')
            preset_02.is_check = True
            preset_02.is_select = False
            preset_02.is_add_collection = False
            preset_02.polycount = 1000

            preset_03 = row.operator('dk.check_hard_poly',
                                     text='2K')
            preset_03.is_check = True
            preset_03.is_select = False
            preset_03.is_add_collection = False
            preset_03.polycount = 2000

            preset_04 = row.operator('dk.check_hard_poly',
                                     text='5K')
            preset_04.is_check = True
            preset_04.is_select = False
            preset_04.is_add_collection = False
            preset_04.polycount = 5000

            preset_05 = row.operator('dk.check_hard_poly',
                                     text='10K')
            preset_05.is_check = True
            preset_05.is_select = False
            preset_05.is_add_collection = False
            preset_05.polycount = 10000
        else:
            prop = col.operator('dk.check_hard_poly',
                                text='Uncheck Polycount')
            prop.is_check = False
            prop.is_select = False
            prop.is_add_collection = False

            col.label(text='- - - - checking - - - -')

            prop_select = col.operator('dk.check_hard_poly',
                                       text='Select Objects')
            prop_select.is_check = False
            prop_select.is_select = True
            prop_select.is_add_collection = False

            prop_col = col.operator('dk.check_hard_poly',
                                    text='Put to Collection')
            prop_col.is_check = False
            prop_col.is_select = False
            prop_col.is_add_collection = True

            # draw list off hard objects
            col.label(text='Objects:')
            hp_obj_dict = dict()
            for i in context.scene.hp_objects:
                hp_obj_dict[i.name] = i.value

            sort_hp_list = sorted([key for key in hp_obj_dict.keys()], reverse=True, key=lambda ob_name: hp_obj_dict[ob_name])
            col = layout.column()
            col.label(text='Hard polycount: {} objects'.format(len(sort_hp_list)))
