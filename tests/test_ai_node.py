import pytest
import uuid
from unittest.mock import patch, MagicMock
from shared.AI_Node import AI_Node


@pytest.fixture
def sample_node():
    """
    Fixture to create a sample AI_Node for testing.
    """
    return AI_Node(
        in_name="TestNode",
        in_node_id=None,
        in_description="This is a test node.",
        in_priority=1,
        in_status="active",
        in_purpose="Test",
        in_task="Initial Task"
    )


@patch("logging.getLogger")
def test_node_initialization_with_uuid(mock_get_logger):
    """
    Test that the node initializes correctly with a generated UUID if no node_id is provided.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    node = AI_Node(
        in_name="Node1",
        in_node_id=None,  # No node ID provided
        in_description="Test description",
        in_priority=5,
        in_status="active",
        in_purpose="Testing",
        in_task="Test Task"
    )

    # Assertions
    assert node.node_id is not None
    assert isinstance(uuid.UUID(node.node_id), uuid.UUID)  # Validate the generated UUID
    assert node.status == "active"
    assert node.priority == 5

def test_node_initialization_with_provided_id():
    """
    Test that the node uses a provided ID instead of generating a new UUID.
    """    
    provided_id = "12345"
    node = AI_Node(
        in_name="Node1",
        in_node_id=provided_id,
        in_description="Test description",
        in_priority=2,
        in_status="inactive",
        in_purpose="Testing",
        in_task="Test Task"
    )

    # Assertions
    assert node.node_id == provided_id
    assert node.status == "inactive"
    assert node.priority == 2

def test_get_details(sample_node):
    """
    Test that the get_details method returns the correct details.
    """

    details = sample_node.get_details()

    # Assertions
    assert details["node_id"] == sample_node.node_id
    assert details["description"] == sample_node.description
    assert details["priority"] == sample_node.priority
    assert details["status"] == sample_node.status
    assert details["purpose"] == sample_node.purpose
    assert details["task"] == sample_node.task

def test_set_status(sample_node):
    """
    Test that the set_status method updates the status correctly.
    """

    sample_node.set_status("inactive")
    assert sample_node.status == "inactive"

def test_str_representation(sample_node):
    """
    Test the string representation of the node.
    """

    result = str(sample_node)

    # Assertions
    assert f"Node({sample_node.node_id}" in result
    assert f"Priority={sample_node.priority}" in result
    assert f"Status={sample_node.status}" in result
    assert f"Purpose={sample_node.purpose}" in result
    assert f"Task={sample_node.task}" in result

def test_set_task(sample_node):
    """
    Test that the set_task method updates the task correctly.
    """

    new_task = "Updated Task"
    sample_node.set_task(new_task)
    assert sample_node.task == new_task

def test_edge_case_empty_description():
    """
    Test that the node handles an empty description.
    """
    node = AI_Node(
        in_name="EdgeNode",
        in_node_id=None,
        in_description="",
        in_priority=1,
        in_status="active",
        in_purpose="Edge Test",
        in_task="Test Task"
    )
    assert node.description == ""

def test_edge_case_invalid_priority():
    """
    Test that the node handles an invalid priority (e.g., negative numbers).
    """
    with pytest.raises(ValueError):
        AI_Node(
            in_name="InvalidNode",
            in_node_id=None,
            in_description="Test description",
            in_priority=-5,  # Invalid priority
            in_status="active",
            in_purpose="Testing",
            in_task="Test Task"
        )

def test_edge_case_null_task():
    """
    Test that the node handles a None task.
    """
    node = AI_Node(
        in_name="EdgeNode",
        in_node_id=None,
        in_description="Test description",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_task=None  # Null task
    )
    assert node.task is None

def test_process_task_mock(sample_node):
    """
    Test the behavior of the process_task method when mocked.
    """
    with patch.object(AI_Node, 'process_task', return_value="Mocked task processed") as mock_method:
        result = sample_node.process_task()

        # Assertions
        assert result == "Mocked task processed"
        mock_method.assert_called_once()  # Ensure the method was called

def test_set_priority():
    """
    Test that set_priority logs an error and raises ValueError for invalid priority.
    Test that set_priority also deals with valid priorities.
    """
    with patch.object(AI_Node, 'log_error') as mock_log_error:
        node = AI_Node(
            in_name="TestNode",
            in_node_id=None,
            in_description="Test Node Description",
            in_priority=1,
            in_status="active",
            in_purpose="Testing",
            in_task="Task"
        )

        # Invalid values
        # Assert that ValueError is raised
        with pytest.raises(ValueError, match="Priority must be greater than or equal to 1."):
            node.set_priority(-5)  # Invalid priority
        # Assert that log_error was called with the correct message
            mock_log_error.assert_called_once_with("Priority must be >= 1")
        with pytest.raises(ValueError, match="Priority must be greater than or equal to 1."):
            node.set_priority(0)  # Invalid priority
            mock_log_error.assert_called_once_with("Priority must be >= 1")
        with pytest.raises(ValueError, match="Priority must be greater than or equal to 1."):
            node.set_priority(-100000000)  # Invalid priority
            mock_log_error.assert_called_once_with("Priority must be >= 1")
        
        # Valid values
        node.set_priority(10)
        assert node.priority == 10
        node.set_priority(1)
        assert node.priority == 1
        node.set_priority(100000)
        assert node.priority == 100000

