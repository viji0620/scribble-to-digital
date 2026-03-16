def create_download_text(corrected_text, todo_list):
    """
    Generate downloadable text content combining corrected text and todo list.
    """
    content = f"Corrected Text:\n{corrected_text}\n\nTodo List:\n"
    if todo_list:
        content += "\n".join(f"- {task}" for task in todo_list)
    else:
        content += "No tasks extracted."
    return content