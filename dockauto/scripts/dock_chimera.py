# chimera dockprep
import sys
import chimera
from chimera import runCommand
from DockPrep import prep

if len(sys.argv) < 3:
    print("[ERROR] Usage: chimera --nogui simple_chimera.py receptor.pdb ligand.pdb")
    sys.exit(1)

receptor_file = sys.argv[-2]
ligand_file   = sys.argv[-1]

print("[INFO] Opening receptor:", receptor_file)
runCommand("open " + receptor_file)

print("[INFO] Opening ligand:", ligand_file)
runCommand("open " + ligand_file)

models = chimera.openModels.list()
receptor = models[0]
ligand   = models[1]

print("[INFO] Running DockPrep on receptor...")
prep([receptor])

print("[INFO] Running DockPrep on ligand...")
prep([ligand])

# Save prepped structures
print("[INFO] Saving prepped receptor and ligand...")
runCommand("write format pdb #0 receptor_prep.pdb")
runCommand("write format pdb #1 ligand_prep.pdb")

print("[INFO] Done. Exiting...")
runCommand("stop now")
