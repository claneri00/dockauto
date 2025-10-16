pymol -cq 1iep_pymol.py
python3 gridbox_searcher.py sti.pdb
python3 create_conf.py sti.pdb 1iep.conf receptor.pdbqt ligand.pdbqt 5.0 12 20 4
chimera --nogui simple_chimera.py 1iep_clean.pdb sti.pdb
obabel ligand_prep.pdb -O ligand.pdbqt 
obabel receptor_prep.pdb -O receptor.pdbqt -p 7.4 --partialcharge gasteiger -xr
./vina --config 1iep.conf >log.txt


pymol -cq 4lxz_pymol.py
python3 gridbox_searcher.py saha.pdb
python3 create_conf.py saha.pdb 4lxz.conf receptor.pdbqt ligand.pdbqt 5.0 12 20 4
chimera --nogui simple_chimera.py 4lxz_clean.pdb saha.pdb
obabel ligand_prep.pdb -O ligand.pdbqt 
obabel receptor_prep.pdb -O receptor.pdbqt -p 7.4 --partialcharge gasteiger -xr
./vina --config 4lxz.conf >log.txt

pymol -cq 1iep_upymol.py -- 1iep


python 0_fetch_pdb.py list.csv #fetch 1 .pdb file for each items in the 1st column of the list (e.g C1.pdb)
pymol -cq 1_pymol.py list.csv #outputs 2 files for each pdb, named C1_receptor.pdb and C1_C2_ligand.pdb

python3 gridbox_searcher.py 3W33_W19_ligand.pdb
python3 create_conf.py 3W33_W19_ligand.pdb 3W33.conf receptor.pdbqt ligand.pdbqt 5.0 12 20 4
chimera --nogui dock_chimera.py 3W33_receptor.pdb 3W33_W19_ligand.pdb
obabel ligand_prep.pdb -O ligand.pdbqt 
obabel receptor_prep.pdb -O receptor.pdbqt -p 7.4 --partialcharge gasteiger -xr
./vina --config 3W33.conf >log.txt
