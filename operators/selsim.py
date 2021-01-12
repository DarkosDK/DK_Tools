import bpy
import bmesh
from mathutils import Vector, Matrix, kdtree
from ..utility.elemutils import BmeshElement
from ..utility.elemutils import split_elements

algorithms = [
    ('By Topology', 'By Topology', 'Select by topology'),
    ('By Indexes', 'By Indexes', 'Select by indexes'),
]


class DK_OP_Select_Similar(bpy.types.Operator):
    bl_idname = "dk.selectsim"
    bl_label = "Select Similar Topology"
    bl_description = "Select similar edges by topology"
    bl_options = {'REGISTER', 'UNDO'}

    algorithm: bpy.props.EnumProperty(
        items=algorithms,
        name="Algorithm",
        default='By Topology',
    )

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            ob = context.active_object
            if (ob is not None) and ob.mode == 'EDIT':
                return bpy.context.tool_settings.mesh_select_mode[1]

    def execute(self, context):

        context = bpy.context

        # Create bmesh
        ob = context.active_object
        mesh = context.object.data
        bm_init = bmesh.from_edit_mesh(mesh) # bm_init
        bm = bm_init.copy()

        # Set containers
        edges_sel = [edge for edge in bm.edges if edge.select]  # Selected edges indecis
        verts_sel = [vert for vert in bm.verts if vert.select]
        edges = [edge for edge in bm.edges]  # All edges indecis
        # elements = dict()  # Conteiner for elements
        # elem_index = 0  # Start index for elements

        # Check if user dont select edges
        if len(edges_sel) == 0:
            self.report({'INFO'}, "Select at least one edge")
            return {'CANCELLED'}

        # Split mesh by elements
        elements = split_elements(bm)
        # print("Elements count: {}".format(len(elements)))

        # Check if user select edges in several (not in one) elements
        element_check = []
        for e in edges_sel:
            for key in elements.keys():
                if e in elements[key]:
                    element_check.append(key)
        element_check = list(set(element_check))
        if len(element_check) != 1:
            self.report({'INFO'}, "Select edges in one element!")
            return {'CANCELLED'}

        # Check if mesh is only one element
        if len(elements) == 1:
            self.report({'INFO'}, "Mesh is only one element")
            return {'CANCELLED'}

        # ! Debugging
        """
        test_edge = edges_sel[0]
        selected_element = None
        need_to_select = []
        for key in elements.keys():
            print('Element {}: {}'.format(key, [e.index for e in elements[key]]))
            if test_edge in elements[key]:
                selected_element = key
                print('Selected edges in element {}'.format(selected_element))
        if selected_element is not None:
            positions = [elements[selected_element].index(e) for e in edges_sel]
            for key in elements.keys():
                if key != selected_element:
                    find_positions = list(map(lambda x: elements[key][x].index, positions))
                    print(find_positions)
                    need_to_select += find_positions

        """
        my_elements = []
        sel_element = None
        for ind in elements.keys():
            my_element = BmeshElement(bm, elements[ind], ind)
            my_elements.append(my_element)
            # print("Element {}: Faces: {}".format(my_element.element_index, [f.index for f in my_element.faces]))
            # print("Element {}: Pivot: {}".format(my_element.element_index, ob.matrix_world @ my_element.pivot))
            # print("Element {}: Identificator: {}".format(my_element.element_index, my_element.ident))
            if my_element.is_active(edges_sel[0].index):
                sel_element = my_element

        my_elements.remove(sel_element)

        # Find similar elements
        similar_elements = []
        for el in my_elements:
            if el.ident == sel_element.ident:
                similar_elements.append(el)
        if len(similar_elements) == 0:
            self.report({'INFO'}, "Not find similar elements")
            return {'CANCELLED'}

        print("Active element is: {}".format(sel_element.element_index))
        print(sel_element.find_sel_indexes())
        # print("Active element scale: {}".format(sel_element.scale_factor))
        # print("Active element normal: {}".format(sel_element.normal))
        # print("Active element up: {}".format(sel_element.up))

        if self.algorithm == 'By Topology':
            # Define selection in similar elements
            to_select = []

            for i in similar_elements:
                # print("Element {} scale: {}".format(i.element_index, i.scale_factor))
                # print("Element {} normal: {}".format(i.element_index, i.normal))
                # print("Element {} up: {}".format(i.element_index, i.up))
                scale = sel_element.scale_factor/i.scale_factor
                m_scale = Matrix.Scale(scale, 4)
                m = Matrix.Translation(sel_element.pivot) @sel_element.matrix.transposed() @ m_scale @ i.matrix @ Matrix.Translation(-i.pivot)
                bmesh.ops.transform(bm, matrix=m, verts=i.verts)

                # create kd-tree
                size = len(i.verts)
                kd = kdtree.KDTree(size)
                for v in i.verts:
                    kd.insert(v.co, v.index)
                kd.balance()

                # define closes vertices to selected 
                for i in verts_sel:
                    co, index, dist = kd.find(i.co)
                    to_select.append(index)

            # print("To Select: {}".format(to_select))

            bm_init.verts.ensure_lookup_table()

            for i in to_select:
                bm_init.verts[i].select = True

            bm_init.select_flush(True)

            # Return bmesh
            bmesh.update_edit_mesh(mesh)
        else:
            to_select = []
            sel_pos = sel_element.find_sel_indexes()

            for el in similar_elements:
                for pos in sel_pos:
                    to_select.append(el.edges[pos].index)

            bm_init.edges.ensure_lookup_table()
            for i in to_select:
                bm_init.edges[i].select = True

            bm_init.select_flush(True)

            # Return bmesh
            bmesh.update_edit_mesh(mesh)
        
        return {'FINISHED'}
