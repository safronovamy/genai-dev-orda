import json
import matplotlib.pyplot as plt
import networkx as nx


# ==========================
# 1. Load JSON data
# ==========================
JSON_PATH = "vocabulary_stats.json"   # ← новое имя файла

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

vocab_stats = data["vocabulary_stats"]


# ==========================
# 2. Build the graph
# ==========================
G = nx.Graph()

EXPLICIT_NODE = "Explicit usage"
IMPLICIT_NODE = "Implicit usage"

G.add_node(EXPLICIT_NODE)
G.add_node(IMPLICIT_NODE)

for item in vocab_stats:
    term = item["term"]
    explicit = item.get("explicit_count", 0)
    implicit = item.get("implicit_count", 0)

    G.add_node(term)

    if explicit > 0:
        G.add_edge(
            term,
            EXPLICIT_NODE,
            weight=explicit,
            usage_type="explicit"
        )

    if implicit > 0:
        G.add_edge(
            term,
            IMPLICIT_NODE,
            weight=implicit,
            usage_type="implicit"
        )


# ==========================
# 3. Layout
# ==========================
pos = nx.spring_layout(G, k=1.5, iterations=200, seed=42)

explicit_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("usage_type") == "explicit"]
implicit_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("usage_type") == "implicit"]

all_weights = [d["weight"] for _, _, d in G.edges(data=True)]
max_weight = max(all_weights) if all_weights else 1

def width_for_edge(u, v):
    w = G[u][v]["weight"]
    return 1.0 + 4.0 * (w / max_weight)

explicit_widths = [width_for_edge(u, v) for u, v in explicit_edges]
implicit_widths = [width_for_edge(u, v) for u, v in implicit_edges]


# ==========================
# 4. Draw the graph
# ==========================
plt.figure(figsize=(13, 9))

nx.draw_networkx_nodes(G, pos, node_size=900)
nx.draw_networkx_labels(G, pos, font_size=8)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=explicit_edges,
    width=explicit_widths,
    edge_color="red",
    alpha=0.8,
    label="Explicit usage"
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=implicit_edges,
    width=implicit_widths,
    edge_color="blue",
    alpha=0.8,
    label="Implicit usage"
)

plt.title("Vocabulary Relationship Graph (Explicit = Red, Implicit = Blue)")
plt.axis("off")
plt.legend(loc="upper left")


# ==========================
# 5. Save PNG
# ==========================
OUTPUT_PATH = "vocabulary_relationship_graph.png"
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=220)
plt.close()

print(f"Graph saved to {OUTPUT_PATH}")