def update_func(self, context):
    wm = context.window_manager
    operator = [op for op in wm.operators if op.name == 'Circle Array']
    # print(context.active_operator)
    if operator:
        operator[-1].rotation_center = context.scene.rotation_center


def create_vector_from_3_points(points):
    center = (points[0] + points[1] + points[2]) / 3
    v1 = points[0] - center
    v2 = points[1] - center
    v = v1.cross(v2)
    return v


def clamp_to_zero(value):
    if value < 0:
        return 0
    else:
        return value


def add_commas(text: str) -> str:
    length = len(text)
    full_part = int(l/3.0)
    fract_part = length % 3

    arr = []

    if fract_part:
        arr.append(text[:fract_part])

    for i in range(full_part):
        arr.append(text[(i*3)+fract_part:(i*3+3)+fract_part])

    final = ','.join(arr)

    return final
