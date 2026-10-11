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
- Brain cortex: "Brain for Blender" by Anderson Winkler (brainder.org), from a real MRI brain, CC BY-SA 3.0, as placed
  in Z-Anatomy; adapted here under CC BY-SA 4.0
- Heart: three valve and papillary parts taken directly from BodyParts3D 4.0 (partof_BP3D_4.0_obj_99.zip)

| File | Contents | From |
|---|---|---|
| `models/skeleton.glb` | 252 bone and costal-cartilage meshes | Z-Anatomy "Skeletal system" (BodyParts3D-derived) |
| `models/organs.glb` | 80 meshes: digestive, respiratory, urinary, male genital and endocrine organs, heart chambers, spleen, diaphragm, eyes | Z-Anatomy "Visceral systems" and others |
| `models/muscles.glb` | 469 muscle and tendon meshes | Z-Anatomy "Muscular system" |
| `models/arteries.glb`, `models/veins.glb` | 423 and 229 vessels (curves turned into tubes) | Z-Anatomy "Cardiovascular system" |
| `models/nerves.glb` | 248 meshes: peripheral and cranial nerves, sympathetic trunk, spinal cord | Z-Anatomy "Nervous system" |
| `models/lymph.glb` | 162 meshes: lymph nodes, thymus, palatine tonsil | Z-Anatomy "Lymphoid organs" |
| `models/brain_*.glb` | cortex (gyri and sulci), deep brain, arteries, cranial nerves, skull (Brain tab) | Brainder via Z-Anatomy; Z-Anatomy |
| `models/heart_*.glb` | chambers, valves, coronary arteries, cardiac veins, great vessels (Heart tab) | Z-Anatomy; BodyParts3D |

Not used:
- Parts that Z-Anatomy bundles under non-commercial terms: the inner ear (University of Dundee, CC BY-NC-SA) and kidney
  (Lissie Cowley, CC BY-NC) models. So the ossicles, cochlea, vestibule, eardrum, auditory tube, cochlear and vestibular
  nerves, renal pelvis and intrarenal vessels are left out, in case they come from those models.
- Z-Anatomy's "White matter of telencephalon", credited to the University of Washington without a license.
- Z-Anatomy's text definitions (from Wikipedia, CC BY-SA 3.0); the cards are our own.
See docs/PLAN_3D.md §Licensing and tools/export_layers.py (`NEVER`).

## Code libraries
- three.js 0.186.1 (`vendor/three/`: core, GLTFLoader, OrbitControls, meshopt decoder), MIT License,
  © 2010–2026 three.js authors. See `vendor/three/LICENSE`.
- KaTeX 0.19.0 (`vendor/katex/`: katex.min.js, katex.min.css, woff2 fonts), MIT License,
  © 2013–2020 Khan Academy and other contributors. See `vendor/katex/LICENSE`. Renders the equations in the MCAT guides.

## MCAT section guides
`content/mcat/guides/*.json` are organized according to the AAMC's *What's on the MCAT Exam?* outline (section
names, foundational concept numbers, content category codes and short names, and the names of the four Scientific
Inquiry and Reasoning Skills are AAMC's framework, used as identifiers). All descriptions, equations as written, and
examples are our own, verified against the open textbooks each topic links to (OpenStax, LibreTexts); the guides
link to those references and never reproduce their text. MCAT® is a registered trademark of the AAMC, which is not
affiliated with and does not endorse this app.

## Chemical structures
Structures in MCAT passages are drawn at build time from SMILES with RDKit (BSD-3-Clause licence, https://www.rdkit.org/) by
`tools/structures.py`; the app ships only the resulting SVG.

## Periodic table
`src/ptable.js` lists the 118 elements with IUPAC standard atomic weights (CIAAW 2024, abridged to one decimal;
elements without a standard weight show the mass number of their longest-lived isotope in brackets, as IUPAC does),
checked against ciaaw.org, NIST and PubChem on 2026-10-11.

## Fonts
Atkinson Hyperlegible (Braille Institute), loaded from Google Fonts, SIL Open Font License 1.1.
