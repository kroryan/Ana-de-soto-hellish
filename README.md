# Ana María de Soto: exclusive custom skin for Marta (Hellish Quart)

A fan-made skin that works only for Marta. It runs on Marta's native 68-joint skeleton (Mafra5/Marfa), with her original moves and rapier. The head and tricorne are rigid. It ships with the Marta first-person (FPP) compatibility adjustment.

## Layout

- `model/AnaMaria_tpose.glb`: the source model in T-pose (tpose muestra 1). It contains PBR textures at 2048 (diffuse, normal, metallic-roughness) and its own 52-bone rig with skin weights.
- `model/*.png`: the four reference images.
- `blender_work/step1_prepare.py`: reads the mesh, rig joints and weights, applies one subdivision level and exports the textures. The glTF MR map (R=1, G=roughness, B=metallic) is used directly as the shader's ORM.
- `blender_work/step3_rig_marta.py`: fits Marta's native skeleton to the source joints, including palm orientation. It renames weights (`Spine1→Spine`, `Spine2→Spine1`), carries the mesh into Marta's bind pose and splits off the rigid head. It exports `Skin.fbx` and QA renders.
- `blender_work/verify_skeleton.py`: checks that `Skin.fbx` holds exactly Marta's 68 bones (names, hierarchy, positions) and that every vertex has valid weights.
- `unity_project/`: Unity 2019.4.0f1 project (menu **AnaMaria → Construir mod**). It builds `skin_marta_anamaria` and `pic_marta_anamaria`. It attaches the controller that hides Marta's stock face, and its shader clears the camera in FPP.
- `release/`: the ZIP contents. These are the four bundles, the installer (`.cmd`/`.ps1`), the FPP patch data and `LEEME.txt`.

## Rebuild

```powershell
$B="C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
& $B -b --factory-startup -P blender_work\step1_prepare.py -- model\AnaMaria_tpose.glb model\AnaMaria_tpose.glb build
& $B -b --factory-startup -P blender_work\step3_rig_marta.py -- build ..\game_reference\MartaSkeleton.json
& $B -b --factory-startup -P blender_work\verify_skeleton.py -- build\marta\Skin.fbx ..\game_reference\MartaSkeleton.json
.\build.ps1
```

## FPP adjustment

The installer changes 4 bytes of Marta's skin loader (PlayMaker FSM, path ID 67770) in `resources.assets`. On Steam build 26432078 the true event of `isFPP?` goes from `yes` to `no`, so first person uses the selected custom skin. Before writing anything, it checks that the 15,936-byte block matches by SHA-256. It saves that block to `marta_loader_backup.bin` and verifies the result. `-Uninstall` restores the original loader when no other Marta custom skin remains installed. The data is in `release/marta_fpp_patch.json`.

`unity_project/Assets/Plugins/PlayMaker.dll` comes from your own game installation and is not meant for redistribution.
