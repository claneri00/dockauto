import sys
import os
import requests
import csv


def fetch_pdb(pdb_id):
    protein_directory = os.path.join("..", "data")

    os.makedirs(protein_directory, exist_ok=True)
    
    pdb_request = requests.get(f"https://files.rcsb.org/download/{pdb_id}.pdb")
    pdb_request.status_code

    with open(f"{protein_directory}/{pdb_id}.pdb", "w+") as f:
        f.write(pdb_request.text)
    
# --- Execution ---
if len(sys.argv) < 2:
    print("Usage: python get_ligand.py <PDB_ID | file.txt | file.csv>")
    sys.exit(1)

arg = sys.argv[1]

pdb_ids = []

# Check if argument is a file
if os.path.isfile(arg):
    if arg.lower().endswith('.csv'):
        # Read first column of CSV
        with open(arg, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip():
                    pdb_ids.append(row[0].strip())
        print(f"Loaded {len(pdb_ids)} PDB IDs from CSV file {arg}")
    else:
        # Treat as plain text file (one ID per line)
        with open(arg, 'r', encoding='utf-8') as f:
            pdb_ids = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(pdb_ids)} PDB IDs from text file {arg}")
else:
    # Single PDB ID
    pdb_ids = [arg.strip()]

# --- Run get_ligands() for each ---
for pdb_id in pdb_ids:
    fetch_pdb(pdb_id)

