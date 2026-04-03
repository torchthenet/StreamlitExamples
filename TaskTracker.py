# -*- coding: utf-8 -*-
# Enhanced TaskTracker with add/delete functionality
import streamlit as st
from datetime import datetime
import json
import uuid

# Define the filename
filename = 'TaskTracker.log'

# Enhanced task data model
def create_task_entry(task, priority="medium", tags=None):
    """Create a new task entry with all required fields"""
    return {
        'id': str(uuid.uuid4()),
        'task': task,
        'start_time': datetime.now().isoformat(),
        'status': 'in_progress',
        'priority': priority.lower(),
        'tags': [tag.strip() for tag in (tags or '').split(',') if tag.strip()]
    }

def log_task(task, start_time=None, priority="medium", tags=None):
    """Log a new task with enhanced metadata"""
    tasks = []
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)
    except:
        pass

    entry = create_task_entry(task, priority, tags)
    tasks.append(entry)
    with open(filename,'w') as file:
        json.dump(tasks, file, indent=2)

    return entry

def read_tasks():
    """Read and return all tasks from the log file, with migration for old formats"""
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)

        # Check if we need to migrate old format
        if tasks and not isinstance(tasks[0], dict):
            # Handle case where tasks is a list of strings (old format)
            migrated_tasks = []
            for task in tasks:
                migrated_tasks.append({
                    'id': str(uuid.uuid4()),
                    'task': task,
                    'start_time': datetime.now().isoformat(),
                    'status': 'todo',
                    'priority': 'medium',
                    'tags': []
                })
            tasks = migrated_tasks

        # Check if tasks are in old format (missing required fields)
        if tasks and 'status' not in tasks[0]:
            tasks = migrate_tasks(tasks)
            save_tasks(tasks)  # Save migrated tasks

        return tasks if tasks else []
    except:
        return []

def save_tasks(tasks):
    """Save tasks to the log file with error handling"""
    try:
        with open(filename, 'w') as file:
            json.dump(tasks, file, indent=2)
        return True
    except Exception as e:
        st.error(f"Failed to save tasks: {str(e)}")
        return False

def migrate_tasks(tasks):
    """Migrate old task format to new format"""
    migrated_tasks = []
    for task in tasks:
        # Create new task entry with default values
        new_task = {
            'id': str(uuid.uuid4()),  # Generate new ID for migrated tasks
            'task': task.get('task', 'Untitled Task'),
            'start_time': task.get('start_time', datetime.now().isoformat()),
            'status': 'todo',  # Default status for migrated tasks
            'priority': 'medium',  # Default priority
            'tags': [],  # Empty tags for migrated tasks
            'end_time': None
        }
        migrated_tasks.append(new_task)
    return migrated_tasks
def update_task_status(task_id, new_status):
    """Update the status of a specific task"""
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            if new_status == 'done':
                task['end_time'] = datetime.now().isoformat()
            save_tasks(tasks)
            return True
    return False

def delete_task(task_id):
    """Delete a task by its ID"""
    tasks = read_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return True

# Streamlit app
st.title('Enhanced Task Logger')

# Add task form
with st.form("add_task_form"):
    st.subheader("Add New Task")
    task_name = st.text_input("Task name", key="task_name")
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"],
        key="priority",
        index=1  # Default to Medium
    )
    tags = st.text_input("Tags (comma-separated)", key="tags")
    submit = st.form_submit_button("Add Task")

    if submit and task_name:
        log_task(task_name, priority=priority, tags=tags)
        st.success(f"Task '{task_name}' added successfully!")

# Task filtering controls
st.subheader("Filter Tasks")
status_filter = st.selectbox(
    "Filter by status",
    ["All", "Todo", "In Progress", "Done"],
    key="status_filter"
)
priority_filter = st.selectbox(
    "Filter by priority",
    ["All", "Low", "Medium", "High"],
    key="priority_filter"
)

# Load and filter tasks
tasks = read_tasks()

# Apply filters
filtered_tasks = [
    task for task in tasks
    if (status_filter == "All" or task['status'] == status_filter.lower())
    and (priority_filter == "All" or task['priority'] == priority_filter.lower())
]

# Display filtered tasks
if filtered_tasks:
    st.subheader(f"Filtered Tasks ({len(filtered_tasks)})")
    for task in reversed(filtered_tasks):
        # Ensure task has all required fields with defaults
        task_display = {
            'task': task.get('task', 'Untitled Task'),
            'status': task.get('status', 'todo'),
            'priority': task.get('priority', 'medium'),
            'tags': task.get('tags', []),
            'start_time': task.get('start_time', datetime.now().isoformat())
        }

        # Display task with safe field access
        with st.expander(f"{task_display['task']} ({task_display['status'].replace('_', ' ').title()})"):
            st.write(f"**Priority:** {task_display['priority'].title()}")
            st.write(f"**Tags:** {', '.join(task_display['tags']) if task_display['tags'] else 'None'}")
            st.write(f"**Started:** {task_display['start_time']}")

            # Status update buttons
            col1, col2, col3 = st.columns(3)
            if col1.button("Mark as Todo"):
                update_task_status(task['id'], 'todo')
                st.rerun()
            if col2.button("Mark as In Progress"):
                update_task_status(task['id'], 'in_progress')
                st.rerun()
            if col3.button("Mark as Done"):
                update_task_status(task['id'], 'done')
                st.rerun()

            # Delete button with confirmation
            if st.button("Delete", key=f"delete_{task['id']}"):
                if st.confirm(f"Are you sure you want to delete '{task_display['task']}'?"):
                    delete_task(task['id'])
                    st.rerun()
else:
    st.info("No tasks found matching your filters.")

# vim: set expandtab tabstop=4 shiftwidth=4 autoindent: