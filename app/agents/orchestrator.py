from typing import Any, Dict
from sqlalchemy.orm import Session
from app import models
from app.agents.task_agent import TaskAgent
from app.agents.schedule_agent import ScheduleAgent
from app.agents.notes_agent import NotesAgent
from app.utils import build_orchestrator_output
from app.mcp_adapter import create_adapter


DEFAULT_RETRIES = 2


class OrchestratorAgent:
    def __init__(self):
        self.task_agent = TaskAgent()
        self.schedule_agent = ScheduleAgent()
        self.notes_agent = NotesAgent()

    def process(self, db: Session, message: str):
        plan = build_orchestrator_output(message)
        execution_results = []
        adapter = create_adapter(db)

        for action in plan["actions"]:
            agent_name = action["agent"]
            tool = action["tool"]
            data = action["input"]

            # Default execution result
            result: Dict[str, Any] = {"agent": agent_name, "tool": tool}

            # Map agent/tool to adapter calls when possible to centralize integrations
            try:
                # Build adapter-style tool name (simple convention)
                adapter_tool = None
                if agent_name == "TaskAgent":
                    adapter_tool = f"tasks.{tool}" if not tool.startswith("tasks.") else tool
                elif agent_name == "ScheduleAgent":
                    adapter_tool = f"calendar.{tool}" if not tool.startswith("calendar.") else tool
                elif agent_name == "NotesAgent":
                    adapter_tool = f"notes.{tool}" if not tool.startswith("notes.") else tool

                if adapter_tool:
                    # Retry loop for transient failures
                    attempt = 0
                    while True:
                        attempt += 1
                        resp = adapter.call(adapter_tool, data)
                        if resp is None or resp.get("error"):
                            if attempt <= DEFAULT_RETRIES:
                                continue
                            result.update({"error": "adapter_error", "detail": resp})
                        else:
                            result.update({"result": resp})
                        break
                else:
                    # fall back to agent-local execution
                    if agent_name == "TaskAgent":
                        result.update(self.task_agent.execute(db, tool, data))
                    elif agent_name == "ScheduleAgent":
                        result.update(self.schedule_agent.execute(db, tool, data))
                    elif agent_name == "NotesAgent":
                        result.update(self.notes_agent.execute(db, tool, data))
                    else:
                        result.update({"error": "Unknown agent"})
            except Exception as e:
                result.update({"error": "exception", "detail": str(e)})

            execution_results.append(result)

            log = models.AgentLog(
                user_query=message,
                agent_used=agent_name,
                action_taken=tool,
                tool_used=tool,
            )
            db.add(log)

        db.commit()

        return {
            "actions": plan["actions"],
            "final_response": plan["final_response"],
            "agents_used": plan["agents_used"],
            "execution_results": execution_results,
        }