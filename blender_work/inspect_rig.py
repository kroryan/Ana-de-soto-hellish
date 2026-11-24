import bpy, sys
src = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
m = bpy.data.objects['model']
print('ARM_MW', [list(r) for r in arm.matrix_world])
print('MODEL_PARENT', m.parent.name if m.parent else None, 'MW', [list(r) for r in m.matrix_world])
print('MODS', [(x.type, getattr(x, 'object', None) and x.object.name) for x in m.modifiers])
print('VGROUPS', len(m.vertex_groups))
for b in arm.data.bones:
    h = arm.matrix_world @ b.head_local; t = arm.matrix_world @ b.tail_local
    print('BONE', b.name, b.parent.name if b.parent else None, tuple(round(x, 3) for x in h), tuple(round(x, 3) for x in t))
mat = m.data.materials[0]
bsdf = mat.node_tree.nodes['Principled BSDF']
print('BASECOLOR', tuple(bsdf.inputs['Base Color'].default_value))
ico = bpy.data.objects['Icosphere']; print('ICO parent', ico.parent and ico.parent.name, ico.location)
