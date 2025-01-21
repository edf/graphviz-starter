"""
creates dataflow diagram
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.generic.os import LinuxGeneral
from diagrams.onprem.client import Users

def create_server_group(count, prefix, node_attr_prefix):
  """
  Creates a group of servers with the given prefix and node attributes

  Args:
    count: The number of servers to create.
    prefix: A string prefix for the server names.
    node_attr_prefix: A string for the node attribute dictionary key.
    
  Returns:
    A list of Server objects.
  """
  servers = []
  for i in range(count):
    server_name = f"{prefix}_{i+1}"
    attr_name = f"{node_attr_prefix}_node_attr"
    server = LinuxGeneral(server_name,style="filled",fillcolor="darkolivegreen2")
    servers.append(server)
  return servers


cloud_graph_attr = {
        "bgcolor": "cadetblue1" 
        }
db_node_attr = {
        "color": "red",
        "style": "filled" 
        }
diagram_graph_attr = {
    "fontsize": "45",
    "labeljust": "L",
    "labelloc": "t",
    "label": "database driven web application\narchitecture",
    "rankdir": "LR",
    "bgcolor": "gainsboro"
    }
lb_node_attr = {
  "style": "filled", 
  "color": "x11grey", 
  "labeljust": "l"
  }
user_graph_attr = {
  "bgcolor": "cadetblue1" 
  }
web_node_attr = {
  "fillcolor": "blue"
  }

with Diagram("Database Driven Web Application Architecture", show=False, graph_attr=diagram_graph_attr):
  with Cluster("users", graph_attr=cloud_graph_attr):
      ext_users = Users("external users", style="filled", color="darkolivegreen3")
      int_users = Users("internal users", style="filled", color="darkolivegreen3")
  with Cluster("cloud", graph_attr=cloud_graph_attr):
    with Cluster("application load balancer"):
        alb = LinuxGeneral("load balancer", **lb_node_attr)
    ext_users >> Edge(label="secure\nconnector") >> alb
    int_users >> Edge(label="secure\nconnector") >> alb
    # Create groups of servers
    with Cluster("web servers"):
      web_servers = create_server_group(9, "web", "web")
    with Cluster("db servers"):
      db_servers = create_server_group(3, "db", "db")
    with Cluster("db load balancer"):
      nlb = LinuxGeneral("load balancer", **lb_node_attr)
    # create connections  
    for i in range(len(web_servers) ):
      alb >> Edge(label="port 443") >> web_servers[i]
    for web_server in web_servers:
      web_server >> nlb 
    for db_server in db_servers:
      nlb >> Edge(label="secure\ndb connector") >> db_server
