#!/bin/bash
# Automate docking workflow for multiple PDB-Ligand pairs
# Usage: ./auto_dock.sh path/to/list.csv

# ================================
# CONFIGURATION
# ================================
BASE_DIR=~/Documents/dockauto
DATA_DIR=$BASE_DIR/data
SCRIPT_DIR=$BASE_DIR/scripts
OUTPUT_DIR=$DATA_DIR/outputs
VINA_BIN="$SCRIPT_DIR/vina"   # vina executable path

# ================================
# GET CSV FILE INPUT
# ================================
if [ -n "$1" ]; then
    CSV_FILE="$1"
else
    read -rp "Enter path to your CSV file: " CSV_FILE
fi

# Expand ~ to $HOME for safety
CSV_FILE="${CSV_FILE/#\~/$HOME}"

if [ ! -f "$CSV_FILE" ]; then
    echo "❌ CSV file not found: $CSV_FILE"
    exit 1
fi

echo "📄 Using CSV file: $CSV_FILE"

# ================================
# FIRST STEP
# ================================
cd "$SCRIPT_DIR" || exit
echo "=== Fetching PDB files ==="
python3 fetch_pdb.py "$CSV_FILE"

echo "=== Cleaning PDB files with PyMOL ==="
pymol -cq clean_pymol.py -- "$CSV_FILE"

# ================================
# SECOND STEP (loop over CSV)
# ================================
while IFS=',' read -r pdbid ligandid chain; do
    echo "==============================="
    echo " Processing: $pdbid (Ligand: $ligandid)"
    echo "==============================="

    FOLDER="$OUTPUT_DIR/$pdbid"

    if [ ! -d "$FOLDER" ]; then
        echo "❌ Folder not found: $FOLDER — skipping"
        continue
    fi

    # Copy required scripts & executables
    echo "📂 Copying required files..."
    cp "$SCRIPT_DIR"/{gridbox_searcher.py,create_conf.py,dock_chimera.py} "$FOLDER"/
    cp "$VINA_BIN" "$FOLDER"/

    cd "$FOLDER" || continue

    # Run docking preparation & docking
    echo "⚙️ Running gridbox_searcher.py..."
    python3 gridbox_searcher.py "${pdbid}_${ligandid}_ligand.pdb"

    echo "⚙️ Creating config file..."
    python3 create_conf.py "${pdbid}_${ligandid}_ligand.pdb" "${pdbid}.conf" receptor.pdbqt ligand.pdbqt 5.0 12 20 4

    echo "⚙️ Running Chimera for docking prep..."
    chimera --nogui dock_chimera.py "${pdbid}_receptor.pdb" "${pdbid}_${ligandid}_ligand.pdb"

    echo "⚙️ Running Open Babel..."
    obabel ligand_prep.pdb -O ligand.pdbqt 
    obabel receptor_prep.pdb -O receptor.pdbqt -p 7.4 --partialcharge gasteiger -xr

    echo "⚙️ Running AutoDock Vina..."
    ./vina --config "${pdbid}.conf" > log.txt

    echo "🧹 Cleaning up temporary .py scripts..."
    rm -f gridbox_searcher.py create_conf.py dock_chimera.py

    echo "✅ Finished $pdbid"
    echo ""
done < "$CSV_FILE"

echo "🎉 All docking jobs completed!"

