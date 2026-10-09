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
- Cranial nerves may derive from "Cranial Nerves and Foramina", University of Dundee, CAHID, CC BY 4.0

| File | Contents | From |
|---|---|---|
| `models/skeleton.glb` | 252 bone and costal-cartilage meshes | Z-Anatomy "Skeletal system" (BodyParts3D-derived) |
| `models/organs.glb` | 80 meshes: digestive, respiratory, urinary, male genital and endocrine organs, heart chambers, spleen, diaphragm, eyes | Z-Anatomy "Visceral systems" and others |
| `models/muscles.glb` | 469 muscle and tendon meshes | Z-Anatomy "Muscular system" |
| `models/arteries.glb`, `models/veins.glb` | 423 and 229 vessels (curves turned into tubes) | Z-Anatomy "Cardiovascular system" |
| `models/nerves.glb` | 248 meshes: peripheral and cranial nerves, sympathetic trunk, spinal cord | Z-Anatomy "Nervous system" |
| `models/lymph.glb` | 162 meshes: lymph nodes, thymus, palatine tonsil | Z-Anatomy "Lymphoid organs" |

Not used:
- Parts that Z-Anatomy bundles under non-commercial terms: the inner ear (University of Dundee, CC BY-NC-SA) and kidney
  (Lissie Cowley, CC BY-NC) models. So the ossicles, cochlea, vestibule, eardrum, auditory tube, cochlear and vestibular
  nerves, renal pelvis and intrarenal vessels are left out, in case they come from those models.
- The brain: Z-Anatomy credits "Brainder" and "White matter" (University of Washington) without a license, so the
  cerebrum, cerebellum and brainstem are left out. The app's Brain tab has its own diagram.
- Z-Anatomy's text definitions (from Wikipedia, CC BY-SA 3.0); the cards are our own.
See docs/PLAN_3D.md §Licensing and tools/export_layers.py (`NEVER`).

## Code libraries
- three.js 0.186.1 (`vendor/three/`: core, GLTFLoader, OrbitControls, meshopt decoder), MIT License,
  © 2010–2026 three.js authors. See `vendor/three/LICENSE`.

## Fonts
Atkinson Hyperlegible (Braille Institute), loaded from Google Fonts, SIL Open Font License 1.1.
