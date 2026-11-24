import bpy, os, sys
from mathutils import Vector
src, out = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
for o in list(bpy.data.objects):
    if o.name == 'Icosphere': bpy.data.objects.remove(o)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x = 800; sc.render.resolution_y = 800
c = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(c); sc.camera = c
c.data.type = 'ORTHO'
for n, pos, tgt, s in [('face', (0, -3, 1.62), (0, 0, 1.62), .32), ('torso', (0, -3, 1.2), (0, 0, 1.2), .7),
                       ('back', (0, 3, 1.4), (0, 0, 1.4), .9), ('side', (3, 0, 1.5), (0, 0, 1.5), .8)]:
    c.data.ortho_scale = s; c.location = pos
    c.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(out, n + '.png'); bpy.ops.render.render(write_still=True)
