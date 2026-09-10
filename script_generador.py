import bpy
import math

# 1. Limpiar escena existente sin usar operadores de interfaz
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh, do_unlink=True)
for cam in bpy.data.cameras:
    bpy.data.cameras.remove(cam, do_unlink=True)
for light in bpy.data.lights:
    bpy.data.lights.remove(light, do_unlink=True)

scene = bpy.context.scene

# 2. Configuración de renderizado optimizado (Cycles CPU - Alta velocidad)
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 16
scene.cycles.max_bounces = 2
scene.cycles.use_denoiser = True

# Formato 9:16 (Vertical Shorts)
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.fps = 30

# 3. Creación de Cámara (Nativa)
cam_data = bpy.data.cameras.new(name="Camara")
cam_obj = bpy.data.objects.new("Camara", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, -8.5, 1.8)
cam_obj.rotation_euler = (math.radians(80), 0, 0)

# 4. Creación de Luz Principal (Nativa)
luz_data = bpy.data.lights.new(name="LuzPrincipal", type='AREA')
luz_data.energy = 1200
luz_data.size_x = 5
luz_data.size_y = 5
luz_obj = bpy.data.objects.new("LuzPrincipal", luz_data)
scene.collection.objects.link(luz_obj)
luz_obj.location = (2, -3, 5)
luz_obj.rotation_euler = (math.radians(35), math.radians(15), 0)

# 5. Creación de Material Dark Noir con Reflexión
mat_piso = bpy.data.materials.new(name="MaterialPiso")
mat_piso.use_nodes = True
nodes = mat_piso.node_tree.nodes
nodes.clear()

node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
node_output = nodes.new(type='ShaderNodeOutputMaterial')
mat_piso.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

# Propiedades del material (Negro mate brillante / Reflejante)
node_principled.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
node_principled.inputs['Roughness'].default_value = 0.15
node_principled.inputs['Metallic'].default_value = 0.8

# 6. Malla del Piso (Construcción NAtiva por vértices sin bpy.ops)
mesh_piso = bpy.data.meshes.new("PisoMesh")
vertices = [(-10, -10, 0), (10, -10, 0), (10, 10, 0), (-10, 10, 0)]
caras = [(0, 1, 2, 3)]
mesh_piso.from_pydata(vertices, [], caras)
mesh_piso.update()

obj_piso = bpy.data.objects.new("Piso", mesh_piso)
obj_piso.data.materials.append(mat_piso)
scene.collection.objects.link(obj_piso)

# 7. Objeto Central de Prueba (Cubo)
mesh_cubo = bpy.data.meshes.new("CuboMesh")
v_cubo = [
    (-1,-1,0), (1,-1,0), (1,1,0), (-1,1,0),
    (-1,-1,2), (1,-1,2), (1,1,2), (-1,1,2)
]
f_cubo = [
    (0,1,2,3), (4,5,6,7), (0,4,5,1),
    (1,5,6,2), (2,6,7,3), (3,7,4,0)
]
mesh_cubo.from_pydata(v_cubo, [], f_cubo)
mesh_cubo.update()

obj_cubo = bpy.data.objects.new("ObjetoPrueba", mesh_cubo)
scene.collection.objects.link(obj_cubo)

print("--- ESCENA GENERADA CORRECTAMENTE SIN OPERADORES BPY.OPS ---")
