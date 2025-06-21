from redis import Redis
from redisgraph import Graph, Node, Edge

class MemoryGraph:
    def __init__(self, host="localhost", port=6379):
        self.redis = Redis(host=host, port=port)
        self.graph = Graph("SlackAIMemory", self.redis)

    def add_message(self, msg_id, text, user, channel, ts):
        # Ensure channel node exists
        self.graph.query(f"MERGE (c:Channel {{name: '{channel}'}})")
        # Add message node
        m = Node(label="Message", properties={
            "id": msg_id, "text": text, "user": user, "ts": ts
        })
        c = Node(label="Channel", properties={"name": channel})
        self.graph.add_node(m)
        self.graph.add_edge(Edge(m, "POSTED_IN", c))
        self.graph.commit()

    def get_recent_context(self, channel, limit=20):
        q = (
            f"MATCH (m:Message)-[:POSTED_IN]->(c:Channel {{name:'{channel}'}}) "
            f"RETURN m.ts, m.text ORDER BY m.ts DESC LIMIT {limit}"
        )
        result = self.graph.query(q)
        texts = [record[1] for record in result.result_set]
        return "\n".join(reversed(texts))
