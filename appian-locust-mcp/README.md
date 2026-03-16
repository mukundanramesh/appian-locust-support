# Appian Locust MCP Server

An MCP server that helps write, debug, improve, and extend Appian Locust performance testing scripts.

## Setup

### 1. Install dependencies

```bash
cd appian-locust-mcp
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 2. Install the steering file

The server uses `appian-locust-steering.md` as its knowledge base. Copy it to the Kiro steering directory:

```bash
mkdir -p ~/.kiro/steering
cp appian-locust-steering.md ~/.kiro/steering/
```

### 3. Configure in Kiro

Add this entry to your `~/.kiro/settings/mcp.json` inside the `"mcpServers"` object:

```json
"appian-locust-mcp": {
  "command": "/absolute/path/to/appian-locust-mcp/.venv/bin/python",
  "args": [
    "/absolute/path/to/appian-locust-mcp/server.py"
  ],
  "env": {
    "APPIAN_LOCUST_REPOS": "https://gitlab.com/your-team/repo1,https://gitlab.example.com/your-team/repo2",
    "APPIAN_LOCUST_SOURCE": "https://gitlab.com/appian-oss/appian-locust",
    "GOOGLE_CHAT_SPACES": "spaces/AAAA1111111,spaces/BBBB2222222"
  },
  "autoApprove": [
    "get_appian_locust_guidance",
    "generate_locust_script",
    "debug_locust_script",
    "search_repo_examples",
    "get_latest_api_reference",
    "search_chat_history",
    "improve_script",
    "explain_workflow"
  ]
}
```

Replace the paths and env values with your actual setup.

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `APPIAN_LOCUST_REPOS` | Comma-separated GitLab repo URLs to search for examples | `https://gitlab.com/team/repo1,https://gitlab.com/team/repo2` |
| `APPIAN_LOCUST_SOURCE` | Official Appian Locust library repo (defaults to `appian-oss/appian-locust`) | `https://gitlab.com/appian-oss/appian-locust` |
| `GOOGLE_CHAT_SPACES` | Comma-separated Google Chat space IDs for searching past discussions | `spaces/AAAA1111111,spaces/BBBB2222222` |

## Tools

| Tool | Description |
|---|---|
| `get_appian_locust_guidance` | Get expert guidance from the steering document, optionally filtered by topic |
| `generate_locust_script` | Generate a script skeleton for a workflow description |
| `debug_locust_script` | Analyze a script for issues and suggest fixes |
| `search_repo_examples` | Search configured GitLab repos for code examples (delegates to GitLab MCP) |
| `get_latest_api_reference` | Look up API reference from the official repo (delegates to GitLab MCP) |
| `search_chat_history` | Search Google Chat for past discussions (delegates to Google Workspace MCP) |
| `improve_script` | Suggest improvements for labels, error handling, validation, stability |
| `explain_workflow` | Explain how to implement a specific Appian workflow type |

## Dependencies

This server delegates repository and chat access to other MCP servers:

- **GitLab MCP server** — for `search_repo_examples` and `get_latest_api_reference`
- **Google Workspace MCP server** — for `search_chat_history`

Make sure those servers are configured in your `mcp.json` alongside this one.

## File Structure

```
appian-locust-mcp/
├── server.py          # MCP server entry point
├── guidance.py        # Steering document loader and search
├── requirements.txt   # Python dependencies
├── .gitignore
└── .venv/             # Virtual environment (not committed)
```
