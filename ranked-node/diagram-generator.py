from diagrams import Diagram, Cluster, Node, Edge

def create_diagram():
    graph_attr = {
        "bgcolor": "cadetblue4",
        "fontname": "Arial",
        "label": "example title for diagram",
        "splines": "ortho",
    }

    node_attr = {
        "shape": "rectangle",
        "fillcolor": "lightgreen",
        "style": "filled",
    }

    with Diagram("My Diagram", show=False, graph_attr=graph_attr, node_attr=node_attr) as diag:
        with Cluster("example cluster 1"):
            a = Node("a", shape="circle")
            group1 = [Node(char) for char in ["b", "c"]]
            a >> Edge(dir="both") >> group1
            
        with Cluster("example cluster 2"):
            i = Node("i", shape="circle", fillcolor="skyblue")
            j = Node("j", fillcolor="skyblue")
            i >> Edge(dir="both") >> j

        a >> Edge(color="white", arrowhead="vee") >> i
    return diag
