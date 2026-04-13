"""Entrypoint for nanobot gateway in Docker.

Reads config.json, injects environment variables, writes config.resolved.json,
then execs into `nanobot gateway`.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config(config_path: str, output_path: str) -> str:
    """Read config, inject env vars, write resolved config."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # LLM provider settings
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config.setdefault("providers", {}).setdefault("custom", {})["apiKey"] = llm_api_key
    if llm_api_base_url:
        config.setdefault("providers", {}).setdefault("custom", {})["apiBase"] = llm_api_base_url
    if llm_api_model:
        config.setdefault("agents", {}).setdefault("defaults", {})["model"] = llm_api_model

    # Gateway settings
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config.setdefault("gateway", {})["host"] = gateway_host
    if gateway_port:
        config.setdefault("gateway", {})["port"] = int(gateway_port)

    # MCP LMS server settings
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if lms_backend_url or lms_api_key:
        mcp_env = config.setdefault("tools", {}).setdefault("mcpServers", {}).setdefault("lms", {}).setdefault("env", {})
        if lms_backend_url:
            mcp_env["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            mcp_env["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Webchat channel settings
    webchat_address = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    nanobot_access_key = os.environ.get("NANOBOT_ACCESS_KEY")

    if webchat_address or webchat_port:
        webchat_config = config.setdefault("channels", {}).setdefault("webchat", {})
        webchat_config["enabled"] = True
        webchat_config.setdefault("allowFrom", ["*"])
        if webchat_address:
            webchat_config["host"] = webchat_address
        if webchat_port:
            webchat_config["port"] = int(webchat_port)
        if nanobot_access_key:
            webchat_config["accessKey"] = nanobot_access_key

    # MCP webchat server settings
    if webchat_address and webchat_port and nanobot_access_key:
        webchat_mcp = config.setdefault("tools", {}).setdefault("mcpServers", {}).setdefault("webchat", {})
        webchat_mcp["command"] = "python"
        webchat_mcp["args"] = ["-m", "mcp_webchat"]
        webchat_mcp["env"] = {
            "NANOBOT_WEBCHAT_UI_RELAY_URL": f"ws://{webchat_address}:{webchat_port}",
            "NANOBOT_WEBCHAT_UI_RELAY_TOKEN": nanobot_access_key,
        }

    # Fix MCP server command to use venv python
    mcp_servers = config.get("tools", {}).get("mcpServers", {})
    for server_name, server_config in mcp_servers.items():
        if isinstance(server_config, dict) and server_config.get("command") == "python":
            server_config["command"] = "/app/.venv/bin/python"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    return output_path


def main() -> None:
    config_path = os.environ.get("NANOBOT_CONFIG_PATH", "/app/nanobot/config.json")
    workspace = os.environ.get("NANOBOT_WORKSPACE", "/app/nanobot/workspace")
    output_path = "/tmp/config.resolved.json"

    # Install mounted MCP packages
    mcp_lms_path = "/app/mcp/mcp-lms"
    if os.path.isdir(mcp_lms_path):
        import subprocess
        result = subprocess.run(
            ["pip", "install", "--no-deps", mcp_lms_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Warning: Failed to install mcp-lms: {result.stderr}", flush=True)
        else:
            print(f"Installed mcp-lms from {mcp_lms_path}", flush=True)

    resolved = resolve_config(config_path, output_path)
    print(f"Using config: {resolved}", flush=True)

    # Replace this process with nanobot gateway
    os.execvp(
        "nanobot",
        ["nanobot", "gateway", "--config", resolved, "--workspace", workspace],
    )


if __name__ == "__main__":
    main()
