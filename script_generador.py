import bpy
import math

def limpiar_escena():
    """Elimina objetos, luces y cámaras previas para evitar conflictos."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def configurar_rendimiento_y_camara():
    """Ajusta la cámara 9:16 y los parámetros para renderizado ultrarrápido en CPU."""
    scene = bpy.context.scene
    
    # Motor de renderizado Cycles en CPU
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    
    # Optimización drástica de velocidad
    scene.cycles.samples = 32  # Bajado de 512/1024 a 32 para renderizar en minutos
    scene.cycles.use_denoiser = True  # Limpia el ruido automático
    
    # Reducción de rebotes de luz (ideal para estilo Dark Noir)
    scene.cycles.max_bounces = 3
    scene.cycles.diffuse_bounces = 2
    scene.cycles.glossy_bounces = 2
    scene.cycles.transparent_max_bounces = 2
    
    # Formato Vertical 9:16
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.fps = 30
    
    # Crear y activar Cámara Principal
    cam_data = bpy.data.cameras.new(name="Camara_Vertical")
    cam_obj = bpy.data.objects.new("Camara_Vertical", cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Encuadre calibrado con Safe Zone (distancia y altura óptima)
    cam_obj.location = (0, -8.5, 1.8)
    cam_obj.rotation_euler = (math.radians(80), 0, 0)
    cam_data.lens = 50

def configurar_iluminacion_y_ambiente():
    """Aplica estética Dark Noir: Fondo texturizado oscuro e iluminación Chiaroscuro."""
    scene = bpy.context.scene
    
    # Fondo ambiental oscuro neutro
    world = scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.02, 0.02, 0.02, 1.0) # Gris casi negro
        bg_node.inputs['Strength'].default_value = 0.5
    
    # Luz Principal Cenital (Key Light) - Alto Contraste
    luz_key_data = bpy.data.lights.new(name="Luz_Key_Data", type='AREA')
    luz_key_data.energy = 800
    luz_key_data.size = 3.0
    luz_key_data.color = (1.0, 0.95, 0.9) # Cálido tenue
    
    luz_key_obj = bpy.data.objects.new("Luz_Key", luz_key_data)
    scene.collection.objects.link(luz_key_obj)
    luz_key_obj.location = (2.5, -3.0, 5.0)
    luz_key_obj.rotation_euler = (math.radians(45), math.radians(15), math.radians(-20))
    
    # Luz de Relleno Suave (Fill Light)
    luz_fill_data = bpy.data.lights.new(name="Luz_Fill_Data", type='AREA')
    luz_fill_data.energy = 150
    luz_fill_data.size = 5.0
    luz_fill_data.color = (0.4, 0.5, 0.7) # Frío tenue
    
    luz_fill_obj = bpy.data.objects.new("Luz_Fill", luz_fill_data)
    scene.collection.objects.link(luz_fill_obj)
    luz_fill_obj.location = (-4.0, -4.0, 3.0)
    luz_fill_obj.rotation_euler = (math.radians(60), 0, math.radians(-45))

def crear_material_mate_oscuro(nombre, color_rgb):
    """Crea materiales estilizados con acabado mate que reflejan la luz dramática."""
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color_rgb
        bsdf.inputs['Roughness'].default_value = 0.6 # Acabado mate
        bsdf.inputs['Metallic'].default_value = 0.1
    return mat

def construir_escena_base():
    """Genera la estructura visual y los pedestales de comparación."""
    # Pared / Fondo oscuro
    bpy.ops.mesh.add_plane(size=20, location=(0, 5, 0))
    fondo = bpy.context.active_object
    fondo.rotation_euler = (math.radians(90), 0, 0)
    mat_fondo = crear_material_mate_oscuro("Mat_Fondo", (0.05, 0.05, 0.06, 1.0))
    fondo.data.materials.append(mat_fondo)
    
    # Plataforma / Pedestal A
    bpy.ops.mesh.add_cylinder(radius=0.8, depth=1.2, location=(-1.2, 0, 0))
    pedestal_a = bpy.context.active_object
    mat_pedestal = crear_material_mate_oscuro("Mat_Pedestal", (0.12, 0.12, 0.14, 1.0))
    pedestal_a.data.materials.append(mat_pedestal)
    
    # Plataforma / Pedestal B
    bpy.ops.mesh.add_cylinder(radius=0.8, depth=1.2, location=(1.2, 0, 0))
    pedestal_b = bpy.context.active_object
    pedestal_b.data.materials.append(mat_pedestal)
    
    # Elemento de acento/comparación central
    bpy.ops.mesh.add_subsurf_cube(radius=0.5, location=(-1.2, 0, 1.1))
    objeto_a = bpy.context.active_object
    mat_objeto_a = crear_material_mate_oscuro("Mat_ObjetoA", (0.8, 0.1, 0.1, 1.0)) # Rojo contraste
    objeto_a.data.materials.append(mat_objeto_a)
    
    bpy.ops.mesh.add_subsurf_cube(radius=0.5, location=(1.2, 0, 1.1))
    objeto_b = bpy.context.active_object
    mat_objeto_b = crear_material_mate_oscuro("Mat_ObjetoB", (0.1, 0.5, 0.9, 1.0)) # Azul contraste
    objeto_b.data.materials.append(mat_objeto_b)

# Ejecución de la escena completa
limpiar_escena()
configurar_rendimiento_y_camara()
configurar_iluminacion_y_ambiente()
construir_escena_base()

print("Escena 3D cargada, iluminada y optimizada correctamente.")
