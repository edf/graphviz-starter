from diagrams import Diagram, Cluster, Node, Edge

# Define global graph attributes
graph_attr = {
    "bgcolor": "cadetblue4",
    "fontname": "Arial",
    "fontcolor": "blue",
    "fontsize": "12",
    "label": "example title for diagram",
    "labelloc": "t",
    "labeljust": "l",
    "splines": "ortho",
    "newrank": "true",
}

# Define default node attributes
node_attr = {
    "fontname": "Arial",
    "fontcolor": "blue",
    "fontsize": "11",
    "shape": "rectangle",
    "fillcolor": "lightgreen",
    "style": "filled",
    "color": "black",
}

# Define default edge attributes
edge_attr = {
    "fontname": "Helvetica",
    "fontcolor": "red",
    "fontsize": "9",
}

with Diagram("\n", show=False, direction="TB", graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr) as diag:
    
    with Cluster("example cluster 1", graph_attr={"fontcolor": "lightgreen"}):
        a = Node("a", shape="circle")
        # Creating b through f
        group1 = [Node(char) for char in ["b", "c", "d", "e", "f"]]
        # dir=both connection
        a >> Edge(dir="both", fillcolor="lightgreen") >> group1

    with Cluster("example cluster 2", graph_attr={"fontcolor": "skyblue"}):
        i = Node("i", shape="circle", fillcolor="skyblue")
        # Creating j through m
        group2 = [Node(char, fillcolor="skyblue") for char in ["j", "k", "l", "m"]]
        # dir=both connection
        i >> Edge(dir="both", fillcolor="skyblue") >> group2

    # Inter-cluster connection
    # Graphviz 'rank' and complex constraints are sometimes handled via 
    # raw DOT injection if the library doesn't expose them directly.
    a >> Edge(dir="both", color="white", penwidth="0.5", arrowhead="vee", arrowtail="vee") >> i

# Note: The 'rank=max' and specific layout tweaks are best handled 
# by the engine when the file is rendered.
