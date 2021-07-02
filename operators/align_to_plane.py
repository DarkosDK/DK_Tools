from ..utility.functions import create_vector_from_3_points
import bpy
import bmesh
from math import radians
from mathutils import Quaternion, Vector


class DK_OT_align_to_plane(bpy.types.Operator):
    """Align object to ortogonal plane by selection"""
    bl_idname = "dk.align_to_plane"
    bl_label = "Align to Plane"
    bl_options = {'REGISTER', 'UNDO'}

    aligne_plane = Vector((0.0, 0.0, -1.0))

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            ob = context.active_object
            return ob is not None and ob.mode == 'EDIT'

    def invoke(self, context, event):
        if context.scene.align_direction == 'X':
            self.aligne_plane = Vector((1.0, 0.0, 0.0))
        elif context.scene.align_direction == '- X':
            self.aligne_plane = Vector((-1.0, 0.0, 0.0))
        elif context.scene.align_direction == 'Y':
            self.aligne_plane = Vector((0.0, 1.0, 0.0))
        elif context.scene.align_direction == '- Y':
            self.aligne_plane = Vector((0.0, -1.0, 0.0))
        elif context.scene.align_direction == 'Z':
            self.aligne_plane = Vector((0.0, 0.0, 1.0))
        return self.execute(context)

    def execute(self, context):

        obj = bpy.context.active_object

        sel_check = False
        sel_mode = bpy.context.tool_settings.mesh_select_mode[:]

        # Get bmesh
        od = obj.data
        bm = bmesh.from_edit_mesh(od)

        # Check Selection
        sel_poly = [p for p in bm.faces if p.select]
        sel_edges = [e for e in bm.edges if e.select]
        sel_verts = [v for v in bm.verts if v.select]
        sel_history = bm.select_history
        active_h = bm.select_history.active
        if len(sel_verts) >= 3 and active_h:
            if sel_mode[0]:
                sel_check = True
            elif sel_mode[1] and len(sel_edges) >= 2:
                sel_check = True
            elif sel_mode[2] and len(sel_poly):
                sel_check = True

        axis = Vector((0.0, 0.0, 0.0))

        if sel_check:
            if sel_mode[0]:
                verts = [v.co for v in sel_history[-3:]]
                v = create_vector_from_3_points(verts)
                v_n = v.normalized()
                inds = [v.index for v in sel_history[-3:]]
                normals = [od.vertices[i].normal for i in inds]
                avr_n = (normals[0] + normals[1] + normals[2]) / 3
                avr_n.normalize()
                if v_n.dot(avr_n) < 0:
                    v = -v
                axis = v
            elif sel_mode[1]:
                es_ind = [e.index for e in sel_history[-2:]]
                v_ind = []
                for e in es_ind:
                    verts_ind = [v for v in od.edges[e].vertices]
                    v_ind += verts_ind
                v_ind = list(set(v_ind))
                verts = [od.vertices[i].co for i in v_ind]
                v = create_vector_from_3_points(verts)
                v_n = v.normalized()
                normals = [od.vertices[i].normal for i in v_ind]
                avr_n = (normals[0] + normals[1] + normals[2]) / 3
                avr_n.normalize()
                if v_n.dot(avr_n) < 0:
                    v = -v
                axis = v
            else:
                p = sel_poly[0].index
                axis = obj.data.polygons[p].normal

        bpy.ops.object.mode_set(mode='OBJECT')
        obj.rotation_mode = 'QUATERNION'
        q = obj.rotation_quaternion
        g_n = axis.copy()
        g_n.rotate(q)

        z = self.aligne_plane
        ang = g_n.angle(z)

        axis_rot = g_n.cross(z)
        rot_q = Quaternion(axis_rot, ang)
        obj.rotation_quaternion = rot_q @ obj.rotation_quaternion

        obj.rotation_mode = 'XYZ'
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}
