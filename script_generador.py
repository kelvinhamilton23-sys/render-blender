import bpy
import math

# 1. Limpieza de escena
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh, do_unlink=True)

scene = bpy.context.scene

# 2. MOTOR EEVEE NEXT (Rasterización pura en GPU para máxima velocidad)
scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Configuraciones de rendimiento extremo
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False

# Resolución nativa Full HD 9:16 (Ya no necesitamos reescalar porque Eevee vuela)
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.fps = 30

# 3. Cámara
cam_data = bpy.data.cameras.new(name="Camara")
cam_obj = bpy.data.objects.new("Camara", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, -8.5, 1.8)
cam_obj.rotation_euler = (math.radians(80), 0, 0)

# 4. Luz
luz_data = bpy.data.lights.new(name="LuzPrincipal", type='AREA')
luz_data.energy = 1500
luz_obj = bpy.data.objects.new("LuzPrincipal", luz_data)
scene.collection.objects.link(luz_obj)
luz_obj.location = (2, -3, 5)

# 5. Piso Reflectante (Dark Noir optimizado para Eevee)
mat_piso = bpy.data.materials.new(name="MaterialPiso")
mat_piso.use_nodes = True
bsdf = mat_piso.node_tree.nodes.get('Principled BSDF')
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['Metallic'].default_value = 0.9

mesh_piso = bpy.data.meshes.new("PisoMesh")
mesh_piso.from_pydata([(-10,-10,0), (10,-10,0), (10,10,0), (-10,10,0)], [], [(0,1,2,3)])
mesh_piso.update()
obj_piso = bpy.data.objects.new("Piso", mesh_piso)
obj_piso.data.materials.append(mat_piso)
scene.collection.objects.link(obj_piso)

# 6. Cubo de Prueba Central
mesh_cubo = bpy.data.meshes.new("CuboMesh")
v = [(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0),(-1,-1,2),(1,-1,2),(1,1,2),(-1,1,2)]
f = [(0,1,2,3),(4,5,6,7),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
mesh_cubo.from_pydata(v, [], f)
mesh_cubo.update()
obj_cubo = bpy.data.objects.new("Cubo", mesh_cubo)
scene.collection.objects.link(obj_cubo)
