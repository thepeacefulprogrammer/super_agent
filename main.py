from minimal_agent_framework import Graph, Node, EventEmitter, tool, context
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

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
        .input("Based on the user_query, provide some quick feedback to indicate how you plan to help. Tell them you can help.")

    )
    research_node = (Node()
        .name("research")
        .input("Tell the user that you have started reseaching to answer their query")
    )
    code_node = (Node()
        .name("code")
        .input("Tell the user that you will write some code to answer their query")
    )

    # define routes
    test_node.routes({
        research_node._id: "you need to do research",
        code_node._id: "the query relates to code"
    })




    return [test_node, research_node, code_node]

if __name__ == "__main__":
    
    events = EventEmitter()
    events.on("text", handler)

    context.events = events

    query = input("User: ")
    context.user_query = query

    graph = Graph()
    nodes = create_nodes()
    graph.add_nodes(nodes)

    graph.run(nodes[0])

