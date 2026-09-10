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

espaciado = 6.0
ancho = 2.2
factor_escala = 0.005

bpy.ops.object.light_add(type='SUN', location=(10, -15, 25))
sun = bpy.context.active_object
sun.data.energy = 4.0

bpy.ops.mesh.add_plane(size=500, location=(0, 0, 0))
suelo = bpy.context.active_object
mat_suelo = bpy.data.materials.new(name="SueloReflectante")
mat_suelo.use_nodes = True
bsdf_suelo = mat_suelo.node_tree.nodes["Principled BSDF"]
bsdf_suelo.inputs["Base Color"].default_value = (0.05, 0.05, 0.07, 1)
bsdf_suelo.inputs["Roughness"].default_value = 0.1
bsdf_suelo.inputs["Metallic"].default_value = 0.8
suelo.data.materials.append(mat_suelo)

total_elementos = len(datos)
for i, item in enumerate(datos):
    pos_x = i * espaciado
    altura = item['valor'] * factor_escala
    
    bpy.ops.mesh.add_cube(location=(pos_x, 0, altura / 2))
    bloque = bpy.context.active_object
    bloque.scale = (ancho / 2, ancho / 2, altura / 2)
    
    mat = bpy.data.materials.new(name=f"Mat_{i}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = item['color']
    bloque.data.materials.append(mat)
    
    bpy.ops.object.text_add(location=(pos_x, -ancho, 0.3))
    txt_nom = bpy.context.active_object
    txt_nom.data.body = item['nombre']
    txt_nom.data.align_x = 'CENTER'
    txt_nom.rotation_euler = (1.5708, 0, 0)
    
    bpy.ops.object.text_add(location=(pos_x, 0, altura + 0.6))
    txt_val = bpy.context.active_object
    txt_val.data.body = f"${item['valor']}B"
    txt_val.data.align_x = 'CENTER'
    txt_val.rotation_euler = (1.5708, 0, 0)
    
    mat_neon = bpy.data.materials.new(name=f"Neon_{i}")
    mat_neon.use_nodes = True
    bsdf_neon = mat_neon.node_tree.nodes["Principled BSDF"]
    bsdf_neon.inputs["Base Color"].default_value = (1, 0.9, 0.3, 1)
    bsdf_neon.inputs["Emission Color"].default_value = (1, 0.8, 0.2, 1)
    bsdf_neon.inputs["Emission Strength"].default_value = 2.0
    txt_val.data.materials.append(mat_neon)

pos_x_final = (total_elementos - 1) * espaciado
bpy.ops.object.camera_add(location=(0, -18, 6))
cam = bpy.context.active_object
cam.rotation_euler = (1.25, 0, 0)
cam.data.lens = 35
scene.camera = cam

cam.keyframe_insert(data_path="location", frame=1)
cam.location.x = pos_x_final
cam.keyframe_insert(data_path="location", frame=1800)

for fcu in cam.animation_data.action.fcurves:
    for kp in fcu.keyframe_points:
        kp.interpolation = 'LINEAR'
"""

with open("generar_vertical.py", "w") as f:
    f.write(blender_code)

print("✅ Script generado con éxito.")
