import json

datos_top = [
    {"nombre": "Empresa J", "valor": 120, "color": [0.8, 0.2, 0.2, 1]},
    {"nombre": "Empresa I", "valor": 210, "color": [0.8, 0.5, 0.2, 1]},
    {"nombre": "Empresa H", "valor": 350, "color": [0.7, 0.8, 0.2, 1]},
    {"nombre": "Empresa G", "valor": 480, "color": [0.2, 0.8, 0.3, 1]},
    {"nombre": "Empresa F", "valor": 610, "color": [0.2, 0.8, 0.8, 1]},
    {"nombre": "Empresa E", "valor": 790, "color": [0.2, 0.4, 0.9, 1]},
    {"nombre": "Empresa D", "valor": 950, "color": [0.5, 0.2, 0.9, 1]},
    {"nombre": "Empresa C", "valor": 1200, "color": [0.9, 0.2, 0.7, 1]},
    {"nombre": "Empresa B", "valor": 1800, "color": [0.9, 0.7, 0.1, 1]},
    {"nombre": "Empresa A", "valor": 2800, "color": [0.9, 0.1, 0.2, 1]}
]

with open("datos_vertical.json", "w") as f:
    json.dump(datos_top, f)

blender_code = """import bpy
import json

with open('datos_vertical.json') as f:
    datos = json.load(f)

bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 1800

collection = scene.collection

# Luz del sol
light_data = bpy.data.lights.new(name="SunLight", type='SUN')
light_data.energy = 4.0
light_obj = bpy.data.objects.new(name="Sun", object_data=light_data)
light_obj.location = (10, -15, 25)
collection.objects.link(light_obj)

# Suelo
mesh_suelo = bpy.data.meshes.new("SueloMesh")
suelo = bpy.data.objects.new("Suelo", mesh_suelo)
collection.objects.link(suelo)

espaciado = 6.0
ancho = 2.2
factor_escala = 0.005
total_elementos = len(datos)

for i, item in enumerate(datos):
    pos_x = i * espaciado
    altura = item['valor'] * factor_escala
    
    # Bloque 3D
    cube_mesh = bpy.data.meshes.new(f"Cube_{i}")
    bloque = bpy.data.objects.new(f"Bloque_{i}", cube_mesh)
    bloque.location = (pos_x, 0, altura / 2)
    bloque.scale = (ancho / 2, ancho / 2, altura / 2)
    collection.objects.link(bloque)
    
    mat = bpy.data.materials.new(name=f"Mat_{i}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = item['color']
    bloque.data.materials.append(mat)

# Cámara
pos_x_final = (total_elementos - 1) * espaciado
cam_data = bpy.data.cameras.new("CameraData")
cam_data.lens = 35
cam = bpy.data.objects.new("Camera", cam_data)
cam.location = (0, -18, 6)
cam.rotation_euler = (1.25, 0, 0)
collection.objects.link(cam)
scene.camera = cam

cam.keyframe_insert(data_path="location", frame=1)
cam.location.x = pos_x_final
cam.keyframe_insert(data_path="location", frame=1800)

if cam.animation_data and cam.animation_data.action:
    for fcu in cam.animation_data.action.fcurves:
        for kp in fcu.keyframe_points:
            kp.interpolation = 'LINEAR'
"""

with open("generar_vertical.py", "w") as f:
    f.write(blender_code)

print("✅ Script generador actualizado correctamente.")
