import requests

def get_ligand_info(pdb_id):
    pdb_id = pdb_id.upper().strip()
    base_url = "https://data.rcsb.org/rest/v1/core"

    # Step 1: Fetch entry metadata
    entry_url = f"{base_url}/entry/{pdb_id}"
    entry_response = requests.get(entry_url)
    if entry_response.status_code != 200:
        print(f"❌ Entry not found for PDB ID '{pdb_id}'")
        return []

    entry_data = entry_response.json()

    # Step 2: Collect all possible ligand-related IDs
    ligand_ids = entry_data.get("rcsb_entry_info", {}).get("nonpolymer_bound_components", [])
    entity_ids = (
        entry_data.get("rcsb_entry_container_identifiers", {}).get("non_polymer_entity_ids", [])
        or entry_data.get("rcsb_entry_container_identifiers", {}).get("nonpolymer_entity_ids", [])
        or []
    )

    ligands = []

    # Step 3: Query all nonpolymer entities
    for eid in entity_ids:
        entity_url = f"{base_url}/nonpolymer_entity/{pdb_id}/{eid}"
        resp = requests.get(entity_url)
        if resp.status_code != 200:
            continue
        entity_data = resp.json()
        chem_ids = entity_data.get("chem_comp_ids", [])
        if not chem_ids:
            continue
        chem_id = chem_ids[0]

        inst_url = f"{base_url}/nonpolymer_entity_instance/{pdb_id}/{eid}"
        inst_resp = requests.get(inst_url)
        chains = []
        if inst_resp.status_code == 200:
            inst_data = inst_resp.json()
            identifiers = inst_data.get("rcsb_nonpolymer_instance_container_identifiers", {})
            chains = identifiers.get("auth_asym_ids", [])
        ligands.append({"ligand_id": chem_id, "chains": chains or ["Unknown"]})

    # Step 4: Fallback: if nothing found, scan polymer_entity_instances for bound ligands
    if not ligands and not ligand_ids:
        polymer_url = f"{base_url}/entry/{pdb_id}"
        data = requests.get(polymer_url).json()
        possible_ligs = data.get("rcsb_entry_info", {}).get("ligand_info", [])
        if possible_ligs:
            ligand_ids = [lig.get("chem_comp_id") for lig in possible_ligs if lig.get("chem_comp_id")]

    # Step 5: Merge unique ligand IDs
    found_ids = set(ligand_ids)
    for lig in ligands:
        if lig["ligand_id"]:
            found_ids.add(lig["ligand_id"])

    if not found_ids:
        print(f"ℹ️ No ligands found for PDB ID '{pdb_id}'")
        return []

    print(f"🔍 Ligands found for {pdb_id}:")
    if ligands:
        for lig in ligands:
            print(f"  • Ligand {lig['ligand_id']} bound to chains: {', '.join(lig['chains'])}")
    else:
        for lid in found_ids:
            print(f"  • Ligand {lid} (chain unknown)")

    return ligands or [{"ligand_id": lid, "chains": ["Unknown"]} for lid in found_ids]


if __name__ == "__main__":
    pdb_id = input("Enter PDB ID: ").strip()
    get_ligand_info(pdb_id)
