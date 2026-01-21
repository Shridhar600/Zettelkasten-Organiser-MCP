import os
import re
import shutil
from fastmcp import FastMCP

# add the root path to the vault plsiz
VAULT_ROOT = "/Users/shridhar600/Documents/Personal/Shridhar"

mcp = FastMCP("Vault Keeper")

def safe_path(relative_path: str) -> str:
    """Ensures the path stays within the vault."""
    full_path = os.path.normpath(os.path.join(VAULT_ROOT, relative_path))
    if not full_path.startswith(os.path.normpath(VAULT_ROOT)):
        raise ValueError("Security Error: Path outside vault root.")
    return full_path
# Test tool
@mcp.tool()
def hello_world(name: str = "World") -> str:
    """Returns a greeting from the Vault Keeper MCP."""
    return f"Hello {name} from Vault Keeper MCP!"

@mcp.tool()
def get_next_id(folder_path: str) -> int:
    """Returns the next available ID from the specified folder (e.g., '002 Project' or '003 TechStack')."""
    target_dir = safe_path(folder_path)
    if not os.path.exists(target_dir):
        return 0 
    
    max_id = 0
    pattern = re.compile(r"^(\d+)")
    for filename in os.listdir(target_dir):
        match = pattern.match(filename)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id
    return max_id + 1

@mcp.tool()
def create_note(path: str, content: str) -> str:
    """Creates a new note at the given path (relative to vault root)."""
    full_path = safe_path(path)
    if os.path.exists(full_path):
        return f"Error: File already exists at {path}"
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Success: Created {path}"

@mcp.tool()
def prepend_text_to_file(file_path: str, text: str) -> str:
    """Prepends text to the beginning of an existing file."""
    full_path = safe_path(file_path)
    if not os.path.exists(full_path):
        return f"Error: File {file_path} not found."
    
    with open(full_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(text + original_content)
    
    return f"Success: Prepended text to {file_path}"

@mcp.tool()
def move_note(source_rel: str, dest_rel: str) -> str:
    """Moves a note from source to destination (both relative to root)."""
    src = safe_path(source_rel)
    dst = safe_path(dest_rel)
    
    if not os.path.exists(src):
        return f"Error: Source {source_rel} not found."
    
    if os.path.exists(dst):
        return f"Error: Destination {dest_rel} already exists. To prevent overwriting, the move has been cancelled."
    
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    return f"Success: Moved {source_rel} to {dest_rel}"

@mcp.tool()
def add_backlink(parent_note_rel: str, note_to_link: str) -> str:
    """Appends a markdown link of 'note_to_link' to the 'parent_note_rel'."""
    parent_path = safe_path(parent_note_rel)
    if not os.path.exists(parent_path):
        return f"Error: Parent note {parent_note_rel} not found."
    
    # note_to_link can be a path we just want the filename without extension for the link
    link_name = os.path.splitext(os.path.basename(note_to_link))[0]
    link_text = f"\n- [[{link_name}]]"
    
    with open(parent_path, "a", encoding="utf-8") as f:
        f.write(link_text)
    return f"Success: Linked {link_name} to {parent_note_rel}"

if __name__ == "__main__":
    mcp.run()
