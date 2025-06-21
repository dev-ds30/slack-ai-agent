import os
from slack_sdk.rtm_v2 import RTMClient
from dotenv import load_dotenv
from memory.graph_store import MemoryGraph
from agents.agent_core import SentientAgent
from suggestions.todo_detector import TodoDetector

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

store = MemoryGraph()
agent = SentientAgent(openai_api_key=OPENAI_API_KEY)
detector = TodoDetector(agent)

@RTMClient.run_on(event="message")
def handle_message(**payload):
    data = payload["data"]
    text = data.get("text")
    user = data.get("user")
    ts   = data.get("ts")
    channel = data.get("channel")

    # 1) Persist to graph
    store.add_message(msg_id=ts, text=text, user=user, channel=channel, ts=ts)

    # 2) Build full context (e.g. last N messages)
    full_context = store.get_recent_context(channel, limit=20)

    # 3) Detect or generate action items
    suggestion = detector.detect(text, full_context)
    if suggestion:
        print("🔔 Suggestion:", suggestion)
        # TODO: post back to Slack or store as ActionItem node

if __name__ == "__main__":
    rtm = RTMClient(token=SLACK_BOT_TOKEN)
    print("Starting Slack‑AI…")
    rtm.start()
