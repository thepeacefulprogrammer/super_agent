from minimal_agent_framework import Graph, Node, EventEmitter, tool
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

for name in ("httpx", "httpcore"):
    lg = logging.getLogger(name)
    lg.setLevel(logging.ERROR)

load_dotenv()

def handler(x: str):
    print(f"{x}", end='', flush=True)

@tool
def get_magic_word() -> str:
    return "pineapple"


def create_nodes() -> list[Node]:

    test_node = (Node()
        .name('test')
        .context_keys(["user_query"])
        .input("Based on the user_query, provide some quick feedback to indicate how you plan to help.")
        .routes([{
            "research": "the query requires research in order to answer",
            "code": "the query is about writing code"
        }])
    )
    
    research_node = (Node()
        .name("research")
        .context_keys(["user_query"])
        .input("Tell the user that you have started reseaching to answer their query")
    )

    code_node = (Node()
        .name("code")
        .context_keys(["user_query"])
        .input("Tell the user that you will write some code to answer their query")
    )

    return [test_node, research_node, code_node]

if __name__ == "__main__":
    
    events = EventEmitter()
    events.on("text", handler)

    context = {
        "user_query": "write a program in python to add 2 numbers together"
    }

    graph = Graph(events)
    nodes = create_nodes()
    graph.add_nodes(nodes)

    graph.run(nodes[0], context)

