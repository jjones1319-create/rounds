"""Chemical structures for MCAT passages, drawn at build time from SMILES with RDKit (BSD-3 licence; see CREDITS.md).
`render_svg(smiles)` returns a trimmed SVG string (no XML header, responsive width) that build.py stores next to the
figure in data/mcat.json, so the app never needs RDKit. `check_smiles` is used by tools/validate.py."""
import re


def _mol(smiles):
    from rdkit import Chem
    return Chem.MolFromSmiles(smiles)


def check_smiles(smiles):
    """None if RDKit parses the SMILES, else an error message."""
    try:
        from rdkit import RDLogger; RDLogger.DisableLog("rdApp.*")
    except ImportError:
        return None
    return None if _mol(smiles) is not None else f"RDKit cannot parse SMILES {smiles!r}"


def render_svg(smiles, width=320, height=220):
    from rdkit.Chem import Draw, rdDepictor
    m = _mol(smiles)
    if m is None: raise ValueError(f"bad SMILES {smiles!r}")
    rdDepictor.Compute2DCoords(m)
    d = Draw.MolDraw2DSVG(width, height)
    o = d.drawOptions(); o.clearBackground = False; o.bondLineWidth = 1.6; o.fixedBondLength = 28; o.padding = 0.08
    d.DrawMolecule(m); d.FinishDrawing()
    svg = d.GetDrawingText()
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
    svg = re.sub(r"<svg([^>]*?)\swidth='\d+px'\sheight='\d+px'", r"<svg\1", svg, count=1)
    svg = svg.replace("<svg", f"<svg width='100%' viewBox='0 0 {width} {height}' role='img'", 1) if "viewBox" not in svg.split(">", 1)[0] else svg.replace("<svg", "<svg width='100%' role='img'", 1)
    svg = re.sub(r"<rect style='opacity:1\.0;fill:#FFFFFF;stroke:none'[^>]*>", "", svg)
    return svg.strip()


if __name__ == "__main__":
    import sys
    print(render_svg(sys.argv[1] if len(sys.argv) > 1 else "OC(=O)c1ccccc1O"))
