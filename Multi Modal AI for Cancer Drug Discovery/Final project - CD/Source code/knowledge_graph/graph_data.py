import networkx as nx


def build_graph():

    G = nx.DiGraph()

    subtypes = ["Indolent-like", "Moderate-like", "Aggressive-like"]

    pathways = [
        "HER2 / ERBB Pathway",
        "PI3K / AKT Pathway",
        "MAPK / ERK Pathway",
        "mTOR Pathway",
        "Cell Cycle Pathway",
        "Apoptosis Pathway",
    ]

    genes = [
        "ERBB2", "ERBB3",
        "PIK3CA", "AKT1",
        "KRAS", "BRAF",
        "MTOR", "RPS6KB1",
        "CDK4", "CCND1",
        "BCL2", "BAX",
    ]

    drugs = [
        "Bortezomib", "Romidepsin", "Sepantronium bromide",
        "Paclitaxel", "Docetaxel",  "Rapamycin",
        "Dactinomycin", "Dinaciclib", "Luminespib",
        "Lapatinib", "Alpelisib", "Gefitinib",
    ]

    for s in subtypes:  G.add_node(s, type="subtype")
    for p in pathways:  G.add_node(p, type="pathway")
    for g in genes:     G.add_node(g, type="gene")
    for d in drugs:     G.add_node(d, type="drug")

    # Subtype → Pathway
    G.add_edge("Indolent-like",   "HER2 / ERBB Pathway",  relation="activates")
    G.add_edge("Indolent-like",   "Apoptosis Pathway",     relation="suppresses")
    G.add_edge("Moderate-like",   "MAPK / ERK Pathway",    relation="activates")
    G.add_edge("Moderate-like",   "mTOR Pathway",          relation="activates")
    G.add_edge("Aggressive-like", "PI3K / AKT Pathway",    relation="activates")
    G.add_edge("Aggressive-like", "Cell Cycle Pathway",    relation="dysregulates")
    G.add_edge("Aggressive-like", "Apoptosis Pathway",     relation="suppresses")

    # Pathway → Gene
    G.add_edge("HER2 / ERBB Pathway",  "ERBB2",    relation="upregulates")
    G.add_edge("HER2 / ERBB Pathway",  "ERBB3",    relation="upregulates")
    G.add_edge("PI3K / AKT Pathway",   "PIK3CA",   relation="mutated_in")
    G.add_edge("PI3K / AKT Pathway",   "AKT1",     relation="activated_by")
    G.add_edge("MAPK / ERK Pathway",   "KRAS",     relation="mutated_in")
    G.add_edge("MAPK / ERK Pathway",   "BRAF",     relation="mutated_in")
    G.add_edge("mTOR Pathway",         "MTOR",     relation="activated_by")
    G.add_edge("mTOR Pathway",         "RPS6KB1",  relation="phosphorylated_by")
    G.add_edge("Cell Cycle Pathway",   "CDK4",     relation="overexpressed")
    G.add_edge("Cell Cycle Pathway",   "CCND1",    relation="amplified")
    G.add_edge("Apoptosis Pathway",    "BCL2",     relation="overexpressed")
    G.add_edge("Apoptosis Pathway",    "BAX",      relation="suppressed")

    # Gene → Drug
    G.add_edge("ERBB2",   "Lapatinib",            relation="targeted_by")
    G.add_edge("ERBB2",   "Bortezomib",           relation="sensitizes")
    G.add_edge("ERBB3",   "Romidepsin",           relation="sensitizes")
    G.add_edge("PIK3CA",  "Alpelisib",            relation="targeted_by")
    G.add_edge("AKT1",    "Sepantronium bromide", relation="inhibited_by")
    G.add_edge("KRAS",    "Gefitinib",            relation="context_for")
    G.add_edge("BRAF",    "Luminespib",           relation="inhibited_by")
    G.add_edge("MTOR",    "Rapamycin",            relation="targeted_by")
    G.add_edge("RPS6KB1", "Docetaxel",            relation="sensitizes")
    G.add_edge("CDK4",    "Dinaciclib",           relation="inhibited_by")
    G.add_edge("CCND1",   "Paclitaxel",           relation="sensitizes")
    G.add_edge("BCL2",    "Dactinomycin",         relation="targeted_by")
    G.add_edge("BAX",     "Bortezomib",           relation="restores")

    return G