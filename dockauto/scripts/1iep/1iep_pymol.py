from pymol import cmd
import os

# Define output paths
ligand_file = os.path.join(os.getcwd(), "sti.pdb")
protein_file = os.path.join(os.getcwd(), "1iep_clean.pdb")

# Clean up old files if they exist
for f in [ligand_file, protein_file]:
    if os.path.exists(f):
        os.remove(f)

# Load the structure
cmd.load("1IEP.pdb", "1IEP")
cmd.remove("solvent")
cmd.remove("chain B")

# Extract ligand (STI)
cmd.select("STI", "resn STI")
cmd.save(ligand_file, "STI")

# Prepare protein: keep only protein chains, then remove chain B
cmd.remove("not polymer.protein")

# Save cleaned protein
cmd.save(protein_file)

