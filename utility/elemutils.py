import bpy
import bmesh
from math import degrees, radians
from mathutils import Vector, Matrix


class BmeshElement:
    def __init__(self, bm, edges, index):
        self.element_index = index
        self.bm = bm
        self.edges = edges
        self.faces = self.define_faces()
        self.verts = self.define_verts()
        self.pivot = self.define_pivot()
        self.normal = self.define_normal()
        self.tangent = self.define_tangent()
        self.up = self.define_up()
        self.matrix = self.define_transform()
        self.ident = self.define_ident()
        self.scale_factor = self.define_scale()
        

    def define_faces(self):
        """
        Define faces of the element by edges
        """
        faces = []
        for edge in self.edges:
            linked_faces = list(edge.link_faces)
            faces += linked_faces
        faces = list(set(faces))

        return sorted(faces, key=lambda x: x.index)

    def define_verts(self):
        vertices = []
        for edge in self.edges:
            linked_verts = list(edge.verts)
            vertices += linked_verts
        vertices = list(set(vertices))

        return sorted(vertices, key=lambda x: x.index)

    def define_pivot(self):
        """
        Define center of mass (in local space)
        """
        all_faces_pos = []
        for face in self.faces:
            pos = face.calc_center_median()
            all_faces_pos.append(pos)
        count = len(all_faces_pos)
        if count == 0:
            count = 1
        pivot = sum(all_faces_pos, Vector((0.0, 0.0, 0.0)))/count
        
        return pivot

    def define_normal(self):
        """
        Define average normal of all element's faces normals
        """
        normals = []
        average_normal = Vector((0.0, 0.0, 0.0))
        for face in self.faces:
            normal = face.normal.normalized()
            normals.append(normal)
        if len(normals) != 0:
            average_normal = sum(normals, Vector((0.0, 0.0, 0.0)))/len(normals)

        if average_normal == Vector((0.0, 0.0, 0.0)):
            average_normal = self.faces[0].normal.normalized()

        return average_normal.normalized()

    def define_tangent(self):
        """
        Define up vector base on the normal and X-axis
        """

        """
        x_axis = Vector((1.0, 0.0, 0.0))
        tangents = []
        average_tangent = Vector((0.0, 0.0, 0.0))
        for face in self.faces:
            tangent = face.calc_tangent_vert_diagonal()
            tangents.append(tangent)
        if len(tangents) != 0:
            average_t = sum(tangents, Vector((0.0, 0.0, 0.0)))/len(tangents)
            average_tangent_01 = average_t.cross(self.normal)
            average_tangent = self.normal.cross(average_tangent_01).normalized()
        """
        """
        # variant 02
        t1 = x_axis.cross(self.normal).normalized()
        t2 = self.normal.cross(t1).normalized()
        # return t2
        """
        # variant 03

        big_faces = []
        max_face = 0
        for face in self.faces:
            if face.calc_area() > max_face:
                max_face = face.calc_area()
        for face in self.faces:
            if face.calc_area() == max_face:
                big_faces.append(face)
        tangents = []
        average_tangent = Vector((0.0, 0.0, 0.0))
        for big in big_faces:
            tangent = face.calc_tangent_vert_diagonal().normalized()
            tangents.append(tangent)

        if len(tangents) != 0:
            average_t = sum(tangents, Vector((0.0, 0.0, 0.0)))/len(tangents)
            if average_t == Vector((0.0, 0.0, 0.0)):
                average_t = self.faces[0].calc_tangent_vert_diagonal().normalized()
            average_tangent_01 = average_t.cross(self.normal)
            average_tangent = self.normal.cross(average_tangent_01).normalized()

        # variant 04
        """
        big_faces = []
        max_face = 0
        for face in self.faces:
            if face.calc_area() > max_face:
                max_face = face.calc_area()
        for face in self.faces:
            if face.calc_area() == max_face:
                big_faces.append(face)
        big = sorted(big_faces, key=lambda x: x.index)
        b = big[0]
        average_t = b.calc_tangent_vert_diagonal()
        average_tangent_01 = average_t.cross(self.normal)
        average_tangent = self.normal.cross(average_tangent_01).normalized()
        """
        return average_tangent

    def define_up(self):
        """
        Create up vector based on normal and tangent
        """

        return self.tangent.cross(self.normal).normalized()

    def define_ident(self):
        """
        Define unique identificator for element
        This value is same for same elements (scale is not affect)
        Include:
            - edges count;
            - angle between faces in each edge
        """
        edges_count = len(self.edges)
        edges_angles = []
        average_angle = 0
        for edge in self.edges:
            angle = degrees(edge.calc_face_angle(0))
            edges_angles.append(angle)
        if len(edges_angles) != 0:
            average_angle = round(sum(edges_angles)/len(edges_angles))

        return (edges_count + average_angle)

    def is_active(self, index):
        """
        Define is the selected edges in this element
        """
        for i in self.edges:
            if i.index == index:
                return True
        return False

    def define_scale(self):
        """
        Define average disnce between pivot and faces
        """
        length = []
        for face in self.faces:
            dist = (self.pivot - face.calc_center_median()).length
            length.append(dist)
        average_dist = 1
        if len(length) != 0:
            average_dist = sum(length)/len(length)

        return average_dist

    def define_transform(self):
        """
        Create Matrix based on average normal, tangent and up vectors
        """
        m = Matrix((self.up, self.tangent, self.normal)).to_4x4()
        return m
        
    def find_sel_indexes(self):
        positions = []
        for pos, e in enumerate(self.edges):
            if e.select == True:
                positions.append(self.edges.index(e))
        return positions


# -- End class

# Utils Functions
def split_elements(bm: bmesh.types.BMesh) -> dict:
    """
    Return dict when geometry split by elements
    key: number of element
    value: list of edges in element
    """
    elements = dict()
    elem_index = 0

    # Set tags to edges
    for e in bm.edges:
        e.tag = False
    edges = [edge for edge in bm.edges]

    # Fill elements dict - put all edges, separate by connected elements
    edges_to_check = edges.copy()
    while edges_to_check:
        to_visit = []
        element = []
        first_edge = edges_to_check[0]
        to_visit.append(first_edge)
        element.append(first_edge)
        edges_to_check.remove(first_edge)
        while to_visit:
            e = to_visit.pop()
            if e.tag:
                continue
            e.tag = True
            for v in e.verts:
                e_linked = [e_l for e_l in v.link_edges if e_l is not e]
                for e_link in e_linked:
                    if not e_link.tag:
                        if e_link not in element:
                            element.append(e_link)
                        if e_link in edges_to_check:
                            edges_to_check.remove(e_link)
                        to_visit.append(e_link)
        elements[elem_index] = sorted(element, key=lambda x: x.index)
        elem_index += 1

    return elements


def find_similar_element(bm: bmesh.types.BMesh, index: int) -> list:
    """
    Find similar elements in bmesh
    """
    pass
