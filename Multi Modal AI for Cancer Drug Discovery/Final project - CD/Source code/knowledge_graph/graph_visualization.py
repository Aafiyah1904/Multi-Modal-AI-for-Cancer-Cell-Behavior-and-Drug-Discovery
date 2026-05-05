from pyvis.network import Network
import tempfile

def visualize_graph(G):

    net = Network(height="600px", width="100%", directed=True)

    for node, data in G.nodes(data=True):

        node_type = data.get("type", "")

        if node_type == "subtype":
            color = "red"
        elif node_type == "pathway":
            color = "orange"
        elif node_type == "gene":
            color = "green"
        else:
            color = "blue"

        net.add_node(node, label=node, color=color)

    for source, target in G.edges():
        net.add_edge(source, target)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(temp_file.name)

    return temp_file.name