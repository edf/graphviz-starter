import pytest
from unittest.mock import patch, MagicMock
from diagram_gen import create_diagram

@patch('diagram_gen.Diagram')
@patch('diagram_gen.Node')
@patch('diagram_gen.Cluster')
def test_diagram_attributes(mock_cluster, mock_node, mock_diagram):
    """Verify that the Diagram is initialized with the correct global styles."""
    create_diagram()
    
    # Check if Diagram was called with the custom background and splines
    args, kwargs = mock_diagram.call_args
    assert kwargs['graph_attr']['bgcolor'] == "cadetblue4"
    assert kwargs['graph_attr']['splines'] == "ortho"
    assert kwargs['node_attr']['fillcolor'] == "lightgreen"

def test_cluster_logic():
    """Verify that we are creating the two specific clusters."""
    with patch('diagram_gen.Cluster') as mock_cluster:
        # We need to mock the context manager behavior
        mock_cluster.return_value.__enter__.return_value = MagicMock()
        
        create_diagram()
        
        # Verify both clusters were initialized
        cluster_names = [call.args[0] for call in mock_cluster.call_args_list]
        assert "example cluster 1" in cluster_names
        assert "example cluster 2" in cluster_names

@patch('diagram_gen.Node')
def test_node_customization(mock_node):
    """Verify that specific nodes get their unique shapes/colors."""
    create_diagram()
    
    # Check if node 'a' and 'i' were created as circles
    # We look for calls where shape='circle' was passed
    circle_nodes = [call.kwargs.get('shape') for call in mock_node.call_args_list]
    assert circle_nodes.count('circle') == 2
    
    # Check for skyblue override in cluster 2
    skyblue_nodes = [call.kwargs.get('fillcolor') for call in mock_node.call_args_list]
    assert "skyblue" in skyblue_nodes
