# Vault Keeper MCP

A simple MCP server that helps organize notes in an Obsidian vault using the Zettelkasten method. Built to work with Gemini CLI and custom Agent Skill.

## What it does

This server gives Gemini CLI the ability to manage your Obsidian notes by:
- Creating and linking notes between parent files (Projects and Tech Stacks)
- Moving notes from a staging area to their proper location
- Maintaining bi-directional links between related notes
- Auto-generating unique IDs for new parent files

## How it works

The server exposes tools that follow a specific workflow (defined in `zettelkasten_organizer_skill/SKILL.md`):
1. Read a new note from the vault root
2. Find or create relevant parent files in `002 Project/` or `003 TechStack/`
3. Create bi-directional links between the note and its parents
4. Move the note to the `Notes/` directory
5. Log the activity

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Update the vault path in `mcp_server.py`:
```python
VAULT_ROOT = "/path/to/your/obsidian/vault"
```

3. Configure Gemini CLI to use this MCP server (add to your MCP config)

## Available Tools

- `read_file` - Read note content
- `glob` - Search for files matching a pattern
- `get_next_id` - Get the next available ID for a folder
- `create_note` - Create a new note
- `add_backlink` - Add a link from parent to child note
- `prepend_text_to_file` - Add text to the beginning of a file
- `move_note` - Move a note from one location to another

## Usage

Just point Gemini CLI at a note in your vault root and ask it to organize it. The skill instructions guide Gemini through the entire process automatically.

## Requirements

- Python 3.13+
- fastmcp
- An Obsidian vault with the expected folder structure
- zettelkasten_organizer skill enabled in Gemini CLI
