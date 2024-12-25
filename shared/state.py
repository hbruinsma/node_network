# shared/state.py
state = {
    "progress": 0,
    "total_tasks": 1,  # Start with 1 for now
    "completed_tasks": 0,
    "nodes": {}
}

# shared/state.py
def register_node(node_name, dependencies=None, priority=0):
    """
    Dynamically register a new node with optional dependencies and priority.
    """
    if node_name not in state["nodes"]:
        state["nodes"][node_name] = {
            "status": "Not Started",
            "dependencies": dependencies or [],
            "retries": 0,
            "output": None,
            "priority": priority
        }

def get_priority(node_name):
    """
    Retrieve the priority of a specific node.
    """
    if node_name in state["nodes"]:
        return state["



# shared/state.py
def add_dependency(node_name, dependency):
    """
    Add a dependency for a specific node.
    """
    if node_name not in state["nodes"]:
        initialize_node(node_name)
    state["nodes"][node_name]["dependencies"] = state["nodes"][node_name].get("dependencies", []) + [dependency]

def get_dependencies(node_name):
    """
    Retrieve the dependencies for a specific node.
    """
    if node_name in state["nodes"]:
        return state["nodes"][node_name].get("dependencies", [])
    return []

def are_dependencies_completed(node_name):
    """
    Check if all dependencies for a specific node are completed.
    """
    dependencies = get_dependencies(node_name)
    for dependency in dependencies:
        if state["nodes"].get(dependency, {}).get("status") != "Completed":
            return False
    return True


# shared/state.py
def increment_retry_count(node_name):
    """
    Increment the retry count for a specific node.
    """
    if node_name in state["nodes"]:
        state["nodes"][node_name]["retries"] = state["nodes"][node_name].get("retries", 0) + 1

def get_retry_count(node_name):
    """
    Get the retry count for a specific node.
    """
    if node_name in state["nodes"]:
        return state["nodes"][node_name].get("retries", 0)
    return 0

def add_feedback(node_name, feedback):
    """
    Add feedback for a node to trigger revisions.
    """
    if node_name in state["nodes"]:
        state["nodes"][node_name]["feedback"] = feedback

def get_feedback(node_name):
    """
    Retrieve feedback for a specific node.
    """
    if node_name in state["nodes"]:
        return state["nodes"][node_name].get("feedback", None)
    return None

def progress_estimation_node():
    """
    Logs the current progress and displays the status of all nodes.
    """
    print("=== Progress Estimation Node ===")
    print(f"Overall Progress: {state['progress']}%")
    print("Node Statuses:")
    for node, details in state["nodes"].items():
        status = details if isinstance(details, str) else details.get("status", "Unknown")
        print(f"  - {node}: {status}")
    print("================================")

def initialize_node(node_name):
    """
    Add a new node to the state with 'Not Started' status.
    """
    state["nodes"][node_name] = "Not Started"
    state["total_tasks"] += 1

def update_node_output(node_name, output):
    """
    Store the output of a specific node in the shared state.
    """
    if node_name in state["nodes"]:
        state["nodes"][node_name] = {"status": "Completed", "output": output}

def update_progress():
    """
    Update the progress percentage based on completed tasks.
    """
    if state["total_tasks"] > 0:
        state["progress"] = int((state["completed_tasks"] / state["total_tasks"]) * 100)

def increment_completed_tasks():
    """
    Increment the count of completed tasks.
    """
    state["completed_tasks"] += 1
    update_progress()

def set_total_tasks(total):
    """
    Set the total number of tasks.
    """
    state["total_tasks"] = total

def update_node_status(node_name, status):
    """
    Update the status of a specific node in the shared state.
    """
    state["nodes"][node_name] = status

def get_node_status(node_name):
    """
    Retrieve the status of a specific node from the shared state.
    """
    return state["nodes"].get(node_name, "Not Started")

def update_progress(progress):
    """
    Update the overall progress of the workflow.
    """
    state["progress"] = progress

def get_progress():
    """
    Retrieve the overall progress of the workflow.
    """
    return state["progress"]
