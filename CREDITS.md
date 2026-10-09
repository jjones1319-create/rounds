# Credits and licenses

## App code and questions
Written for this project. The owner chooses the license for these (add a LICENSE file at the repo root).
Questions are original and cite the guidelines they were checked against in each explanation.

## 3D anatomy models
Model files in `models/` are derived from the sources below and are licensed **CC BY-SA 4.0**
(see `models/LICENSE`, which also lists the changes made). Keep this list complete whenever a model file is added or changed.

- BodyParts3D, The Database Center for Life Science, CC BY-SA 2.1 Japan
- Z-Anatomy, the libre 3D atlas of anatomy (Gauthier Kervyn, Marcin Zielinski), CC BY-SA 4.0
  (source: Z-Anatomy.zip at commit bb293be4 of github.com/Z-Anatomy/Models-of-human-anatomy)

| File | Contents | From |
|---|---|---|
| `models/skeleton.glb` | 252 bone and costal-cartilage meshes | Z-Anatomy "Skeletal system" (BodyParts3D-derived) |

Not used (non-commercial licenses): parts that Z-Anatomy bundles under NC terms, such as the inner ear
(University of Dundee) and kidney (Lissie Cowley) models. The auditory ossicles are left out of the skeleton
for the same reason (they may come from the Dundee inner-ear model). See docs/PLAN_3D.md §Licensing.
Z-Anatomy's text definitions (from Wikipedia) are not used; the cards are our own.

## Code libraries
- three.js 0.186.1 (`vendor/three/`: core, GLTFLoader, OrbitControls, meshopt decoder), MIT License,
  © 2010–2026 three.js authors. See `vendor/three/LICENSE`.

## Fonts
Atkinson Hyperlegible (Braille Institute), loaded from Google Fonts, SIL Open Font License 1.1.
