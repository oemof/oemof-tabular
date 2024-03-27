import matplotlib.pyplot as plt
import networkx as nx


def plot_bev_results(energysystem, facade_label):
    if not isinstance(facade_label, list):
        facade_label = [facade_label]

    # energysystem.results[list(energysystem.results)[0]]
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    for c, r in energysystem.results.items():
        if not r["sequences"].empty:
            if isinstance(c, tuple):
                try:
                    name = str([i.label for i in c])
                except AttributeError:
                    name = "None"
            else:
                name = c
            try:
                for key in facade_label:
                    if key in c[0].label or key in c[1].label:
                        ax = ax1
                    else:
                        ax = ax2
                    column = [
                        i for i in r["sequences"].columns if ("flow" in i)
                    ]
                    # r["sequences"]["flow"].plot(ax=ax, label=c)
                    r["sequences"][column].plot(ax=ax, label=c)
            except:
                print(c)
                pass

    ax1.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
    ax1.set_title("Controlled")
    # plt.tight_layout()
    fig1.show()

    ax2.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
    ax2.set_title("Other")
    plt.tight_layout()
    fig2.show()

    fig, ax = plt.subplots(figsize=(10, 8))
    energysystem.new_results["shortage: el-bus"]["sequences"].plot(
        ax=ax, label="shortage"
    )
    energysystem.new_results["el-bus: excess"]["sequences"].plot(
        ax=ax, label="excess"
    )
    ax.set_title("Excess and shortage")
    ax.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
    plt.tight_layout()
    fig.show()

    for key in facade_label:
        energysystem.new_results[f"{key}-storage: {key}-bus"][
            "sequences"
        ].plot(ax=ax, label="storage: internal-bus")
    ax.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
    ax.set_title("Storage")
    plt.tight_layout()
    fig.show()

    fig, ax = plt.subplots(figsize=(10, 8))
    for key in facade_label:
        if "V2G" in key:
            energysystem.new_results[f"{key}-v2g: el-bus"]["sequences"].plot(
                ax=ax, label=f"{key}-v2g"
            )
    ax.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
    ax.set_title("V2G to el-bus")
    plt.tight_layout()
    fig.show()

    fig, ax = plt.subplots(figsize=(10, 8))
    for key in facade_label:
        energysystem.new_results[f"{key}-2pkm: pkm-bus"]["sequences"].plot(
            ax=ax, label=f"{key}-2pkm-bus"
        )
    ax.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
    ax.set_title("Flows 2 pkm-bus")
    plt.tight_layout()
    fig.show()


def draw_graph(energysystem):
    # Draw the graph
    def assign_color(nodes):
        node_colors = list()
        for n in nodes:
            if "BEV_V2G" in n:
                node_colors.append("firebrick")
            elif "BEV_G2V" in n:
                node_colors.append("lightblue")
            elif "BEV_inflex" in n:
                node_colors.append("darkviolet")
            elif "excess" in n:
                node_colors.append("green")
            elif "shortage" in n:
                node_colors.append("yellow")
            elif "load" in n:
                node_colors.append("orange")
            elif "wind" in n:
                node_colors.append("pink")
            elif "bus" in n:
                node_colors.append("grey")
            elif "pkm_demand" in n:
                node_colors.append("dodgerblue")
            else:
                node_colors.append("violet")
        return node_colors

    from oemof.network.graph import create_nx_graph

    G = create_nx_graph(energysystem)

    # Specify layout and draw the graph
    pos = nx.drawing.nx_agraph.graphviz_layout(
        G, prog="neato", args="-Gepsilon=0.0001"
    )

    fig, ax = plt.subplots(figsize=(20, 16))
    node_colors = assign_color(list(G.nodes()))

    nx.draw(
        G,
        pos,
        # **options,
        with_labels=True,
        node_size=3000,
        # node_color='lightblue',
        font_size=10,
        font_weight="bold",
        node_color=node_colors,
        # node_color=["red", "blue", "green", "yellow", "orange"],
    )

    squares = [n for n in G.nodes() if "storage" in n]
    square_colors = assign_color(squares)

    # Draw square nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=squares,
        node_shape="s",  # Square shape
        node_size=3000,
        node_color=square_colors,  # Assign colors based on the list
    )

    diamonds = [n for n in G.nodes() if "conversion" in n or "v2g" in n]
    diamond_colors = assign_color(diamonds)

    # Draw square nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=diamonds,
        node_shape="D",  # Square shape
        node_size=3000,
        node_color=diamond_colors,  # Assign colors based on the list
    )

    triangle_circles = [n for n in G.nodes() if "demand" in n]
    dtriangle_circle_colors = assign_color(triangle_circles)

    # Draw square nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=triangle_circles,
        node_shape="^",  # Square shape
        node_size=3000,
        node_color=dtriangle_circle_colors,  # Assign colors based on the list
    )

    labels = nx.get_edge_attributes(G, "weight")
    # Adjust label positions
    # label_pos = {key: (value[0], value[1] - 1e8) for key, value in pos.items()}  # Lower the y-coordinate

    nx.draw_networkx_edge_labels(
        G, pos=pos, edge_labels=labels, verticalalignment="top"
    )

    # Customize the plot as needed
    ax.set_title("Energy System Graph for BEV Flett")

    # Show the plot
    plt.show()
