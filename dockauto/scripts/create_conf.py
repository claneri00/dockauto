import sys
import os
from gridbox_searcher import get_gridbox_from_ligand

template = """receptor = {receptor}
ligand = {ligand}
out = {out}

center_x = {center_x}
center_y = {center_y}
center_z = {center_z}
size_x = {size_x}
size_y = {size_y}
size_z = {size_z}

energy_range = {energy_range}
exhaustiveness = {exhaustiveness}
num_modes = {num_modes}
"""

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python3 make_conf.py ligand.pdb output.conf receptor.pdbqt ligand.pdbqt [padding] [exhaustiveness] [num_modes] [energy_range]")
        sys.exit(1)

    ligand_file = sys.argv[1]
    out_file = sys.argv[2]
    receptor_file = sys.argv[3]
    ligand_pdbqt = sys.argv[4]

    padding = float(sys.argv[5]) if len(sys.argv) > 5 else 5.0
    exhaustiveness = int(sys.argv[6]) if len(sys.argv) > 6 else 8
    num_modes = int(sys.argv[7]) if len(sys.argv) > 7 else 9
    energy_range = int(sys.argv[8]) if len(sys.argv) > 8 else 3

    if not os.path.isfile(ligand_file):
        print(f"Error: {ligand_file} not found.")
        sys.exit(1)

    params = get_gridbox_from_ligand(ligand_file, padding=padding)
    params.update({
        "receptor": receptor_file,
        "ligand": ligand_pdbqt,
        "out": "result.pdbqt",
        "exhaustiveness": exhaustiveness,
        "num_modes": num_modes,
        "energy_range": energy_range,
    })

    with open(out_file, "w") as f:
        f.write(template.format(**params))

    print(f"Wrote docking config to {out_file}")

