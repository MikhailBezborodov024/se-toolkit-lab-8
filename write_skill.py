skill_content = '''---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS MCP tools that provide real-time data from the Learning Management System backend. Use these tools to answer questions about labs, learners, and performance metrics.

## Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `lms_health` | Check if LMS backend is healthy and get item count | None |
| `lms_labs` | List all available labs | None |
| `lms_learners` | List all registered learners | None |
| `lms_pass_rates` | Get pass rates (avg score + attempt count per task) for a lab | `lab` (lab ID) |
| `lms_timeline` | Get submission timeline (date + submission count) for a lab | `lab` (lab ID) |
| `lms_groups` | Get group performance (avg score + student count per group) for a lab | `lab` (lab ID) |
| `lms_top_learners` | Get top learners by average score for a lab | `lab` (lab ID), `limit` (default 5) |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | `lab` (lab ID) |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline | None |

## Strategy

### When the user asks about scores, pass rates, completion, groups, timeline, or top learners:

1. **If no lab is specified:**
   - First call `lms_labs` to get available labs
   - If multiple labs exist, ask the user to choose one
   - Present labs with their full titles (e.g., "Lab 01 – Products, Architecture & Roles")

2. **If a lab is specified:**
   - Call the appropriate tool (`lms_pass_rates`, `lms_completion_rate`, etc.)
   - If the tool fails, try `lms_sync_pipeline` first, then retry

### When the user asks "what can you do?":

Explain your current capabilities clearly:
- "I can query the LMS backend for real-time data about labs, learners, and performance."
- "I can show you pass rates, completion rates, group performance, top learners, and submission timelines for any lab."
- "I can also check if the LMS backend is healthy."
- "Just ask me about any lab metric, and I'll fetch the live data for you."

### Formatting results:

- Present numeric results clearly: percentages, counts, averages
- Use tables or bullet points for structured data
- Keep responses concise but informative
- Always mention which lab the data is for

### Handling missing information:

- If a required parameter (like lab ID) is missing, ask the user to specify
- Don't guess or assume lab IDs — always use `lms_labs` first if unsure
- If the user provides an invalid lab ID, show them the list from `lms_labs`

## Examples

**User:** "Show me the scores"
**You:** Call `lms_labs` first, then ask: "Which lab would you like to see scores for? Here are the available labs: [list from lms_labs]"

**User:** "What's the pass rate for lab-04?"
**You:** Call `lms_pass_rates` with `lab: "lab-04"` and format the results

**User:** "Is the backend working?"
**You:** Call `lms_health` and report the status and item count
'''

with open('nanobot/workspace/skills/lms/SKILL.md', 'w', encoding='utf-8') as f:
    f.write(skill_content)
print('SKILL.md written successfully')
