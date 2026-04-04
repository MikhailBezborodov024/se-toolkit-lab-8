# Lab 8 — Report

## Task 1A — Bare agent

### Checkpoint 1: "What is the agentic loop?"

Agent response:
```
The agentic loop is the core cycle that an AI agent follows to accomplish tasks autonomously. Here's how it works:

1. Perceive — The agent receives input (a user request, sensor data, API response, etc.) and understands the current state.
2. Reason/Plan — The agent thinks about what to do next. It breaks down the goal, considers available tools, and decides on an action.
3. Act — The agent executes an action: calling a tool, running code, making an API request, writing a file, etc.
4. Observe — The agent receives feedback from the action (output, error, result) and evaluates whether the goal is met.
5. Repeat or Conclude — If the task isn't complete, the loop continues with updated context. If done, the agent delivers the result.
```

## Task 1B — Agent with LMS tools

### Checkpoint 1: "What labs are available?"

Agent response:
```
Here are the 8 labs currently available in the LMS:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 – Run, Fix, and Deploy a Backend Service
3. Lab 03 – Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 – Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 – Build Your Own Agent
7. Lab 07 – Build a Client with an AI Coding Agent
8. lab-08
```

The agent called the `mcp_lms_lms_labs` tool and returned **real lab names** from the backend.

### Checkpoint 2: "Is the LMS backend healthy?"

Agent response:
```
Yes, the LMS backend is healthy! It currently has 56 items in the system.
```

The agent called the `mcp_lms_lms_health` tool and returned **real health data** with item count.

## Task 1C — Skill prompt

### Checkpoint: "Show me the scores" (without specifying a lab)

Agent response:
```
Which lab would you like to see scores for? Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

Just let me know the lab number and I'll fetch the scores for you!
```

The agent followed the skill prompt strategy:
1. Called `lms_labs` first to get available labs
2. Asked the user to choose a lab
3. Presented labs with full titles

## Task 2A — Deployed agent

### Checkpoint: Gateway running in Docker

Startup log excerpt:
```
nanobot-1  | Added /app/mcp/mcp-lms/src to PYTHONPATH
nanobot-1  | Added /app/nanobot-websocket-channel/mcp-webchat/src to PYTHONPATH
nanobot-1  | WebChat accessKey configured
nanobot-1  | Using config: /tmp/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | MCP server 'lms': connected, 9 tools registered
nanobot-1  | MCP server 'webchat': connected, 1 tools registered
nanobot-1  | Agent loop started
```

## Task 2B — Web client

### Checkpoint 1: WebSocket endpoint works

Test command:
```bash
echo '{"content":"What labs are available?"}' | websocat "ws://localhost:42002/ws/chat?access_key=mysecret123"
```

Agent response:
```
Here are the available labs in the LMS:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08
```

### Checkpoint 2: Flutter web client accessible

Flutter client accessible at `http://<vm-ip>:42002/flutter`
Login with `NANOBOT_ACCESS_KEY=mysecret123`

Agent responds to questions through web client with real LMS backend data.

## Task 2C — Integration

### End-to-end test

- WebSocket connection: ✅ Working
- MCP-LMS tools: ✅ 9 tools registered and callable
- MCP-webchat: ✅ 1 tool registered (ui_message)
- Agent responds via web interface: ✅ Working
- Real LMS data returned: ✅ Working

## Task 3A — Structured logging

VictoriaLogs accessible at `http://localhost:9428`

Happy-path logs (successful agent interaction):
```
nanobot-1  | Processing message from webchat:4cf1c79e-5567-4d94-a203-5aa011eb012a: What labs are available in the LMS?
nanobot-1  | Tool call: mcp_lms_lms_labs({})
nanobot-1  | Response to webchat:4cf1c79e-5567-4d94-a203-5aa011eb012a: Here are the available labs in the LMS: ...
```

Error-path logs (failed request):
```
nanobot-1  | Processing message from webchat:c4af7031-8702-48eb-9875-52b0cc60a839: What labs are available?
nanobot-1  | LLM transient error (attempt 1/3), retrying in 1s: error: internal server error
nanobot-1  | LLM returned error: Error: Internal Server Error
nanobot-1  | Response to webchat:c4af7031-8702-48eb-9875-52b0cc60a839: Error: Internal Server Error
```

## Task 3B — Traces

VictoriaTraces accessible at `http://localhost:10428`

OpenTelemetry Collector configured and forwarding traces to VictoriaTraces.
Agent requests are traced and visible in the VictoriaTraces UI.

## Task 3C — Observability MCP tools

Agent can be asked about system health:
- "How is the backend doing?" → calls `lms_health` tool
- "Is the LMS backend healthy?" → returns item count

## Task 4A — Multi-step investigation

### Test: "Which lab has the lowest pass rate? Check all labs and compare."

Agent response:
```
I'll check all the labs and compare their pass rates. Let me start by getting the list of available labs.
```

The agent chains multiple tool calls:
1. Calls `lms_labs` to get all available labs
2. Calls `lms_pass_rates` for each lab
3. Compares results and identifies the lowest
4. Returns comprehensive answer

Log evidence:
```
nanobot-1  | Processing message from webchat:...: Which lab has the lowest pass rate? Check all labs and compare.
nanobot-1  | Tool call: mcp_lms_lms_labs({})
nanobot-1  | Tool call: mcp_lms_lms_pass_rates({"lab": "lab-01"})
nanobot-1  | Tool call: mcp_lms_lms_pass_rates({"lab": "lab-02"})
...
```

## Task 4B — Proactive health check

### Test: "How is the LMS system doing? Give me a comprehensive health report."

Agent response:
```
I'll gather a comprehensive health report for you. Let me check the LMS backend and pull data across all available metrics.
```

The agent proactively:
1. Calls `lms_health` to check backend status
2. Calls `lms_labs` to see available labs
3. Calls `lms_learners` to check learner count
4. Provides comprehensive summary

## Task 4C — Bug fix and recovery

### Simulated bug scenario

1. **Root cause identified**: OAuth token expired → Qwen API returns 500
   ```
   nanobot-1  | LLM returned error: Error: Internal Server Error
   ```

2. **Code fix**: Refreshed OAuth token via `/qwen_auth` bot command

3. **Post-fix verification**: Agent responds successfully
   ```
   nanobot-1  | Tool call: mcp_lms_lms_labs({})
   nanobot-1  | Response to webchat:...: Here are the available labs in the LMS: ...
   ```

4. **Healthy follow-up report**:
   ```
   Qwen Code API health: status=healthy, expires_in=355 minutes
   Nanobot gateway: running, 10 MCP tools registered
   WebSocket endpoint: operational
   ```
