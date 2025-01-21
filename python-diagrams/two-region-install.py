"""
two region overview
"""
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.generic.database import _Database
from diagrams.generic.network import Firewall
import datetime

# customize filename 
timestamp = datetime.datetime.now().strftime("%Y-%m%d-%H%M")
print(timestamp)
filename = "bc-cluster-" + str(timestamp)

# add graphviz attributes 
diagram_graph_attr = {
    "fontsize": "45",
    "labeljust": "c",
    "labelloc": "t",
    "label": "high level overview\nof HA/DR on AWS",
    "rankdir": "LR",
    "bgcolor": "gainsboro"
    }

with Diagram("high level HA/DR on AWS", show=False, filename=filename, graph_attr=diagram_graph_attr):

    with Cluster("region two"):
      # Primary Site
      with Cluster("region2 Primary Availability Zone"):
        r2_primary_hana = EC2("SAP HANA (Primary)")
        r2_primary_node1 = EC2("RHEL 9 Node 1")
        r2_primary_node2 = EC2("RHEL 9 Node 2")
        r2_primary_node1 >> r2_primary_hana
        r2_primary_node2 >> r2_primary_hana

      # Secondary Site
      with Cluster("region 2 Secondary Availability Zone"):
        r2_secondary_hana = EC2("SAP HANA (Secondary)")
        r2_secondary_node1 = EC2("RHEL 9 Node 1")
        r2_secondary_node2 = EC2("RHEL 9 Node 2")
        r2_secondary_node1 >> r2_secondary_hana
        r2_secondary_node2 >> r2_secondary_hana
      # AWS Services
      with Cluster("region 2 Storage"):
        r2_aws_s3 = S3("S3 (Backups)")

      # Security
      with Cluster("region 2 Security"):
        r2_firewall = Firewall("Firewall")
        r2_firewall >> Edge(color="blue", style="dashed") >> r2_primary_node1
        r2_firewall >> Edge(color="blue", style="dashed") >> r2_primary_node2
        r2_firewall >> Edge(color="blue", style="dashed") >> r2_secondary_node1
        r2_firewall >> Edge(color="blue", style="dashed") >> r2_primary_hana
        r2_firewall >> Edge(color="blue", style="dashed") >> r2_secondary_hana

    # Connections
    r2_primary_hana >> Edge(label="System Replication") >> r2_secondary_hana
    r2_primary_node1 >> Edge(label="High Availability") >> r2_primary_node2
    r2_secondary_node1 >> Edge(label="High Availability") >> r2_secondary_node2

    r2_primary_node1 >> Edge(color="green") >> r2_aws_s3
    r2_primary_node2 >> Edge(color="green") >> r2_aws_s3 
    r2_secondary_node1 >> Edge(color="green") >> r2_aws_s3
    r2_secondary_node2 >> Edge(color="green") >> r2_aws_s3
    r2_primary_hana >> Edge(color="green") >> r2_aws_s3
    r2_secondary_hana >> Edge(color="green") >> r2_aws_s3


    with Cluster("region one"):
      # Primary Site
      with Cluster("Primary Availability Zone"):
        primary_hana = EC2("SAP HANA (Primary)")
        primary_node1 = EC2("RHEL 9 Node 1")
        primary_node2 = EC2("RHEL 9 Node 2")
        primary_node1 >> primary_hana
        primary_node2 >> primary_hana

      # Secondary Site
      with Cluster("Secondary Availability Zone"):
        secondary_hana = EC2("SAP HANA (Secondary)")
        secondary_node1 = EC2("RHEL 9 Node 1")
        secondary_node2 = EC2("RHEL 9 Node 2")
        secondary_node1 >> secondary_hana
        secondary_node2 >> secondary_hana
      # AWS Services
      with Cluster("Storage"):
        aws_s3 = S3("S3 (Backups)")

      # Security
      with Cluster("Security"):
        firewall = Firewall("Firewall")
        firewall >> Edge(color="blue", style="dashed") >> primary_node1
        firewall >> Edge(color="blue", style="dashed") >> primary_node2
        firewall >> Edge(color="blue", style="dashed") >> secondary_node1
        firewall >> Edge(color="blue", style="dashed") >> secondary_node2
        firewall >> Edge(color="blue", style="dashed") >> primary_hana
        firewall >> Edge(color="blue", style="dashed") >> secondary_hana

    # Connections
    primary_hana >> Edge(label="System Replication") >> secondary_hana
    primary_node1 >> Edge(label="High Availability") >> primary_node2
    secondary_node1 >> Edge(label="High Availability") >> secondary_node2

    primary_node1 >> Edge(color="green") >> aws_s3
    primary_node2 >> Edge(color="green") >> aws_s3 
    secondary_node1 >> Edge(color="green") >> aws_s3
    secondary_node2 >> Edge(color="green") >> aws_s3
    primary_hana >> Edge(color="green") >> aws_s3
    secondary_hana >> Edge(color="green") >> aws_s3
