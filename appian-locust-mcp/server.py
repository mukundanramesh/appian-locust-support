#!/usr/bin/env python3
"""Appian Locust MCP Server — expert assistant for Appian Locust scripting."""

import asyncio
import os
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from guidance import load_steering, search_steering

server = Server("appian-locust-mcp")

# ── Config from env ────────────────────────────────────────────────

def _parse_csv(val: str) -> list[str]:
    return [x.strip() for x in val.split(",") if x.strip()] if val else []

REPOS = _parse_csv(os.getenv("APPIAN_LOCUST_REPOS", ""))
SOURCE_REPO = os.getenv("APPIAN_LOCUST_SOURCE", "https://gitlab.com/appian-oss/appian-locust")
CHAT_SPACES = _parse_csv(os.getenv("GOOGLE_CHAT_SPACES", ""))

for r in REPOS:
    if not (r.startswith("https://") and "gitlab" in r.lower()):
        raise ValueError(f"Invalid GitLab URL: {r}")

# ── Tools ──────────────────────────────────────────────────────────

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_appian_locust_guidance",
            description="Get expert guidance on Appian Locust scripting from the steering document. Optionally filter by topic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic to filter (e.g. 'login', 'grid', 'record', 'task', 'form')"}
                }
            }
        ),
        Tool(
            name="generate_locust_script",
            description="Generate an Appian Locust script skeleton for a workflow description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {"type": "string", "description": "Workflow description"},
                    "site": {"type": "string", "description": "Appian site name (optional)"},
                    "page": {"type": "string", "description": "Appian page name (optional)"},
                },
                "required": ["workflow"]
            }
        ),
        Tool(
            name="debug_locust_script",
            description="Analyze an Appian Locust script for issues and suggest fixes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {"type": "string", "description": "The Locust script source code"},
                    "error": {"type": "string", "description": "Error message or traceback (optional)"},
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="search_repo_examples",
            description="Search configured GitLab repos for Appian Locust code examples. Delegates to the GitLab MCP server.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to search for"},
                    "file_pattern": {"type": "string", "description": "File pattern filter (default: *.py)"},
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_latest_api_reference",
            description="Get API reference info from the official Appian Locust repo. Delegates to the GitLab MCP server.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {"type": "string", "description": "Class name (e.g. SailUiForm, AppianTaskSet, Visitor)"},
                    "method_name": {"type": "string", "description": "Method name (optional)"},
                }
            }
        ),
        Tool(
            name="search_chat_history",
            description="Search Google Chat spaces for past Appian Locust discussions. Delegates to Google Workspace MCP.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "issue_type": {"type": "string", "description": "Issue type filter (e.g. error, timeout, login)"},
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="improve_script",
            description="Suggest improvements for an Appian Locust script (labels, error handling, validation, stability).",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {"type": "string", "description": "The Locust script source code"},
                    "focus_areas": {
                        "type": "array", "items": {"type": "string"},
                        "description": "Areas to focus on (e.g. error_handling, reporting, stability)"
                    },
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="explain_workflow",
            description="Explain how to implement a specific Appian workflow type in Locust.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_type": {"type": "string", "description": "Workflow type (e.g. login, task completion, record interaction)"},
                    "details": {"type": "string", "description": "Additional details"},
                },
                "required": ["workflow_type"]
            }
        ),
    ]

# ── Tool handlers ──────────────────────────────────────────────────

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:

    if name == "get_appian_locust_guidance":
        result = search_steering(arguments.get("topic", ""))
        return [TextContent(type="text", text=result)]

    if name == "generate_locust_script":
        guidance = search_steering("script generation")
        script = _build_script_skeleton(
            arguments["workflow"],
            arguments.get("site", ""),
            arguments.get("page", ""),
        )
        return [TextContent(type="text", text=f"{script}\n\n---\n# Relevant Guidance\n\n{guidance[:2000]}")]

    if name == "debug_locust_script":
        analysis = _analyze_script(arguments["script"], arguments.get("error", ""))
        return [TextContent(type="text", text=analysis)]

    if name == "search_repo_examples":
        result = _repo_search_instructions(arguments["query"], arguments.get("file_pattern", "*.py"))
        return [TextContent(type="text", text=result)]

    if name == "get_latest_api_reference":
        result = _api_ref_instructions(arguments.get("class_name", ""), arguments.get("method_name", ""))
        return [TextContent(type="text", text=result)]

    if name == "search_chat_history":
        result = _chat_instructions(arguments["query"], arguments.get("issue_type", ""))
        return [TextContent(type="text", text=result)]

    if name == "improve_script":
        result = _suggest_improvements(arguments["script"], arguments.get("focus_areas", []))
        return [TextContent(type="text", text=result)]

    if name == "explain_workflow":
        guidance = search_steering(arguments["workflow_type"])
        details = arguments.get("details", "")
        text = f"# {arguments['workflow_type'].title()} Workflow\n\n"
        if details:
            text += f"{details}\n\n"
        text += f"## Guidance\n\n{guidance}\n\n"
        text += "## References\n- https://appian-locust.readthedocs.io/\n- https://gitlab.com/appian-oss/appian-locust\n"
        return [TextContent(type="text", text=text)]

    raise ValueError(f"Unknown tool: {name}")


# ── Helpers ────────────────────────────────────────────────────────

def _build_script_skeleton(workflow: str, site: str, page: str) -> str:
    lines = [
        "from locust import HttpUser, task",
        "from appian_locust import AppianTaskSet",
        "",
        "",
        "class MyTaskSet(AppianTaskSet):",
        f'    """Workflow: {workflow}"""',
        "",
        "    @task",
        "    def run_workflow(self):",
    ]
    wl = workflow.lower()
    if site and page:
        lines.append(f'        form = self.appian.visitor.visit_site("{site}", "{page}")')
    elif "task" in wl:
        lines.append('        form = self.appian.visitor.visit_task("Task Name")  # Update')
    elif "record" in wl:
        lines.append('        form = self.appian.visitor.visit_record_instance("RecordType", "RecordName")  # Update')
    elif "report" in wl:
        lines.append('        form = self.appian.visitor.visit_report("Report Name")  # Update')
    elif "action" in wl:
        lines.append('        form = self.appian.visitor.visit_action("Action Name")  # Update')
    else:
        lines.append('        form = self.appian.visitor.visit_site("SiteName", "PageName")  # Update')

    if any(k in wl for k in ("fill", "enter", "input", "form")):
        lines.append('        form.fill_text_field(label="Field", value="Value")  # Update')
    if any(k in wl for k in ("submit", "save", "complete")):
        lines.append('        form.click_button(label="Submit")  # Update')
    if "grid" in wl:
        lines.append('        form.select_rows_in_grid(rows=[0], label="Grid")  # Update')

    lines += [
        "",
        "",
        "class UserActor(HttpUser):",
        "    tasks = [MyTaskSet]",
        "    host = 'https://mysite.appiancloud.com'  # Update",
        '    auth = ["username", "password"]  # Update',
    ]
    return "\n".join(lines)


def _analyze_script(script: str, error: str) -> str:
    issues, fixes = [], []
    if "AppianTaskSet" not in script:
        issues.append("Not extending AppianTaskSet")
        fixes.append("Use `class MyTaskSet(AppianTaskSet):`")
    if "@task" not in script:
        issues.append("No @task decorator")
        fixes.append("Add `@task` to test methods")
    if "self.appian" not in script and "AppianTaskSet" in script:
        issues.append("Not using self.appian client")
        fixes.append("Use `self.appian.visitor` for navigation")
    if error:
        el = error.lower()
        if "not found" in el or "keyerror" in el:
            fixes.append("Try exact_match=False or use test labels (is_test_label=True)")
        if "login" in el or "auth" in el:
            fixes.append("Check host format (no https://) and credentials")
        if "timeout" in el:
            fixes.append("Increase timeout or add refresh loops for async content")

    parts = ["# Script Analysis\n"]
    if issues:
        parts.append("## Issues\n" + "\n".join(f"- {x}" for x in issues) + "\n")
    if fixes:
        parts.append("\n## Suggestions\n" + "\n".join(f"- {x}" for x in fixes) + "\n")
    if error:
        guidance = search_steering(error.split("\n")[0][:50])
        parts.append(f"\n## Related Guidance\n\n{guidance[:1500]}\n")
    if not issues and not error:
        parts.append("No obvious issues found. Script structure looks correct.\n")
    return "\n".join(parts)


def _suggest_improvements(script: str, focus_areas: list) -> str:
    items = []
    if "locust_request_label" not in script:
        items.append(("Reporting", "Add custom request labels", 'form.click_button(label="Submit", locust_request_label="Workflow.Submit")'))
    if "is_test_label" not in script:
        items.append(("Stability", "Use test labels instead of display labels", 'form.fill_text_field(label="emp_name", value="John", is_test_label=True)'))
    if "try:" not in script:
        items.append(("Error Handling", "Add try/except blocks", 'try:\n    form.click_button(label="Submit")\nexcept Exception as e:\n    self.logger.error(f"Failed: {e}")\n    raise'))
    if "assert" not in script:
        items.append(("Validation", "Add validation checks", "form.assert_no_validations_present()"))

    parts = ["# Improvement Suggestions\n"]
    for area, desc, example in items:
        parts.append(f"\n## {area}: {desc}\n```python\n{example}\n```\n")
    return "\n".join(parts) if items else "Script already follows best practices."


def _repo_search_instructions(query: str, file_pattern: str) -> str:
    parts = [f"# Search Repos for: {query}\n"]
    if REPOS:
        parts.append("Use the **GitLab MCP server** (`search_code` or `get_file_content`) on:\n")
        for repo in REPOS:
            path = repo.replace("https://gitlab.com/", "")
            parts.append(f"- Project `{path}` — search for `{query}`, filter `{file_pattern}`\n")
    else:
        parts.append("⚠️ No repos configured. Set APPIAN_LOCUST_REPOS env var.\n")
    source_path = SOURCE_REPO.replace("https://gitlab.com/", "")
    parts.append(f"\nAlso check official source `{source_path}` in `appian_locust/` directory.\n")
    return "".join(parts)


def _api_ref_instructions(class_name: str, method_name: str) -> str:
    source_path = SOURCE_REPO.replace("https://gitlab.com/", "")
    file_map = {
        "SailUiForm": "appian_locust/uiform.py",
        "AppianTaskSet": "appian_locust/appian_task_set.py",
        "AppianClient": "appian_locust/appian_client.py",
        "Visitor": "appian_locust/visitor.py",
    }
    parts = [f"# API Reference\n\nUse **GitLab MCP server** on project `{source_path}`:\n"]
    if class_name and class_name in file_map:
        parts.append(f"- Fetch file: `{file_map[class_name]}`\n")
        if method_name:
            parts.append(f"- Search for: `def {method_name}`\n")
    elif class_name:
        parts.append(f"- Search code for: `class {class_name}`\n")
    else:
        for cls, path in file_map.items():
            parts.append(f"- `{cls}` → `{path}`\n")
    parts.append("\nDocs: https://appian-locust.readthedocs.io/\n")
    return "".join(parts)


def _chat_instructions(query: str, issue_type: str) -> str:
    parts = [f"# Chat Search: {query}\n"]
    if CHAT_SPACES:
        search_q = f"{query} {issue_type}".strip() if issue_type else query
        parts.append("Use **Google Workspace MCP server** (`search_messages`) on:\n")
        for space in CHAT_SPACES:
            parts.append(f"- Space `{space}` — query: `{search_q}`\n")
        parts.append("\nLook for similar errors, workarounds, and config fixes.\n")
    else:
        parts.append("⚠️ No chat spaces configured. Set GOOGLE_CHAT_SPACES env var.\n")
    return "".join(parts)


# ── Entry point ────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="appian-locust-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
