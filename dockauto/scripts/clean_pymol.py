from pymol import cmd
import os
import sys
import csv

# --- Handle command-line argument ---
if len(sys.argv) < 2:
    print("Usage: pymol -cq 1_pymol.py -- <input.csv>")
    sys.exit(1)

csv_file = sys.argv[1]
if not os.path.exists(csv_file):
    print(f"Error: file '{csv_file}' not found.")
    sys.exit(1)

# --- Directory containing the CSV and PDB files ---
data_dir = os.path.dirname(os.path.abspath(csv_file))

# --- Root output directory ---
output_root = os.path.join(data_dir, "outputs")
os.makedirs(output_root, exist_ok=True)

# --- Process each entry in the CSV ---
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row or len(row) < 3:
            continue  # skip blank or incomplete rows

        pdb_id = row[0].strip()
        ligand_name = row[1].strip()
        chain_to_keep = row[2].strip()

        print(f"\nProcessing {pdb_id} | Ligand: {ligand_name} | Chain: {chain_to_keep}")

        pdb_path = os.path.join(data_dir, f"{pdb_id}.pdb")
        
        # Create a specific subfolder for each PDB ID
        output_dir = os.path.join(output_root, pdb_id)
        os.makedirs(output_dir, exist_ok=True)

        ligand_file = os.path.join(output_dir, f"{pdb_id}_{ligand_name}_ligand.pdb")
        receptor_file = os.path.join(output_dir, f"{pdb_id}_receptor.pdb")

        if not os.path.exists(pdb_path):
            print(f"⚠️ Skipping {pdb_id} — file not found: {pdb_path}")
            continue

        # Reset PyMOL to avoid leftover objects
        cmd.reinitialize()

        # Load structure
        cmd.load(pdb_path, pdb_id)

        # Remove solvent
        cmd.remove("solvent")

        # Remove all chains except the desired one
        cmd.remove(f"not chain {chain_to_keep}")

        # Extract ligand
        cmd.select(ligand_name, f"resn {ligand_name}")
        cmd.save(ligand_file, ligand_name)

        # Keep only protein
        cmd.remove("not polymer.protein")

        # Save receptor
        cmd.save(receptor_file)

        print(f"✅ Saved ligand:   {ligand_file}")
        print(f"✅ Saved receptor: {receptor_file}")

print("\n✅ All entries processed successfully!")
