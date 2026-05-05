import networkx as nx

SUBTYPE_MAP = {
    "Indolent-like": {
        "pathways": ["HER2 / ERBB Pathway", "Apoptosis Pathway"],
        "genes": {
            "HER2 / ERBB Pathway": ["ERBB2", "ERBB3"],
            "Apoptosis Pathway":   ["BCL2",  "BAX"],
        },
        "drugs": {
            "ERBB2": ["Bortezomib", "Lapatinib"],
            "ERBB3": ["Romidepsin"],
            "BCL2":  ["Sepantronium bromide"],
            "BAX":   ["Bortezomib"],
        },
    },
    "Moderate-like": {
        "pathways": ["MAPK / ERK Pathway", "mTOR Pathway"],
        "genes": {
            "MAPK / ERK Pathway": ["KRAS",    "BRAF"],
            "mTOR Pathway":       ["MTOR",    "RPS6KB1"],
        },
        "drugs": {
            "KRAS":    ["Gefitinib"],
            "BRAF":    ["Luminespib"],
            "MTOR":    ["Rapamycin"],
            "RPS6KB1": ["Docetaxel", "Paclitaxel"],
        },
    },
    "Aggressive-like": {
        "pathways": ["PI3K / AKT Pathway", "Cell Cycle Pathway"],
        "genes": {
            "PI3K / AKT Pathway": ["PIK3CA", "AKT1"],
            "Cell Cycle Pathway": ["CDK4",   "CCND1"],
        },
        "drugs": {
            "PIK3CA": ["Alpelisib"],
            "AKT1":   ["Sepantronium bromide"],
            "CDK4":   ["Dinaciclib"],
            "CCND1":  ["Paclitaxel", "Dactinomycin"],
        },
    },
}


def build_subtype_graph(subtype: str) -> nx.DiGraph:
    if subtype not in SUBTYPE_MAP:
        raise ValueError(f"Unknown subtype '{subtype}'. Choose from: {list(SUBTYPE_MAP.keys())}")

    data = SUBTYPE_MAP[subtype]
    G = nx.DiGraph()

    G.add_node(subtype, type="subtype")

    for pathway in data["pathways"]:
        G.add_node(pathway, type="pathway")
        G.add_edge(subtype, pathway, relation="activates")

    for pathway, gene_list in data["genes"].items():
        for gene in gene_list:
            G.add_node(gene, type="gene")
            G.add_edge(pathway, gene, relation="involves")

    for gene, drug_list in data["drugs"].items():
        for drug in drug_list:
            G.add_node(drug, type="drug")
            G.add_edge(gene, drug, relation="targeted_by")

    return G