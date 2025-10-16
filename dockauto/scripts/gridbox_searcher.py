import numpy as np

#usage: python3 gridbox_searcher.py ligand.pdb
import numpy as np
import sys
import os

def get_gridbox_from_ligand(ligand_pdb, padding=5.0):
    xs, ys, zs = [], [], []
    
    # Read PDB and collect atomic coordinates
    with open(ligand_pdb) as f:
        for line in f:
            if line.startswith(("HETATM", "ATOM")):
                xs.append(float(line[30:38]))
                ys.append(float(line[38:46]))
                zs.append(float(line[46:54]))
    
    xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)
    
    # Grid box center
    center_x = (xs.max() + xs.min()) / 2.0
    center_y = (ys.max() + ys.min()) / 2.0
    center_z = (zs.max() + zs.min()) / 2.0
    
    # Grid box size (add padding around ligand)
    size_x = (xs.max() - xs.min()) + padding
    size_y = (ys.max() - ys.min()) + padding
    size_z = (zs.max() - zs.min()) + padding
    
    return {
        "center_x": round(center_x, 3),
        "center_y": round(center_y, 3),
        "center_z": round(center_z, 3),
        "size_x": round(size_x, 3),
        "size_y": round(size_y, 3),
        "size_z": round(size_z, 3),
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gridbox_searcher.py ligand.pdb [padding]")
        sys.exit(1)

    ligand_file = sys.argv[1]
    if not os.path.isfile(ligand_file):
        print(f"Error: {ligand_file} not found.")
        sys.exit(1)

    padding = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    
    params = get_gridbox_from_ligand(ligand_file, padding=padding)
    print("Docking grid parameters for:", ligand_file)
    for k, v in params.items():
        print(f"{k} = {v}")


