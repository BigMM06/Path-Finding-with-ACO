import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# ==================================================
# Draw Ant
# ==================================================

def draw_ant(ax, row, col):

    x = col
    y = row

    # Abdomen
    ax.scatter(
        x - 0.13, y,
        color="#8B1E1E",
        s=100,
        zorder=10
    )

    # Thorax
    ax.scatter(
        x, y,
        color="#B52B2B",
        s=65,
        zorder=10
    )

    # Head
    ax.scatter(
        x + 0.13, y,
        color="#C83232",
        s=80,
        zorder=10
    )

    # Legs
    for side in [-1, 1]:

        ax.plot(
            [x - 0.02, x - 0.12],
            [y, y + side * 0.15],
            color="black",
            linewidth=1.5,
            zorder=9
        )

        ax.plot(
            [x + 0.02, x + 0.10],
            [y, y + side * 0.15],
            color="black",
            linewidth=1.5,
            zorder=9
        )

    # Antennae
    ax.plot(
        [x + 0.15, x + 0.20],
        [y - 0.05, y - 0.15],
        color="black",
        linewidth=1.3,
        zorder=10
    )


# ==================================================
# Draw Pheromone Information Panel
# ==================================================

def draw_pheromones(ax, pheromones, position):

    ax.clear()
    ax.axis("off")

    ax.set_title(
        "Pheromone Values",
        fontsize=15,
        fontweight="bold",
        pad=20
    )

    if position is None:

        ax.text(
            0.5, 0.5,
            "No ant position",
            ha="center",
            va="center",
            fontsize=11,
            transform=ax.transAxes
        )

        return

    row, col = position

    # Get pheromone values at current cell
    values = [
        ("Up", pheromones[row, col, 0]),
        ("Down", pheromones[row, col, 1]),
        ("Left", pheromones[row, col, 2]),
        ("Right", pheromones[row, col, 3])
    ]

    ax.text(
        0.5, 0.90,
        f"Current cell: ({row}, {col})",
        ha="center",
        fontsize=11,
        transform=ax.transAxes
    )

    # Display four directions
    for i, (direction, value) in enumerate(values):

        y = 0.73 - i * 0.16

        ax.text(
            0.08,
            y,
            f"{direction}:",
            fontsize=12,
            transform=ax.transAxes
        )

        ax.text(
            0.92,
            y,
            f"{value:.4f}",
            fontsize=12,
            fontweight="bold",
            ha="right",
            transform=ax.transAxes
        )

        # Separator
        ax.plot(
            [0.08, 0.92],
            [y - 0.06, y - 0.06],
            color="gray",
            alpha=0.4,
            transform=ax.transAxes
        )


# ==================================================
# Main Visualization
# ==================================================

def show_visualization(problem, history):

    if not history:

        print("There are no steps to display.")
        return

    current_step = 0

    # Create grid and pheromone panel
    fig, (ax, pheromone_ax) = plt.subplots(
        1,
        2,
        figsize=(13, 8),
        gridspec_kw={
            "width_ratios": [3, 1]
        }
    )

    plt.subplots_adjust(
        bottom=0.2,
        wspace=0.3
    )

    # ==================================================
    # Find Current Ant Position
    # ==================================================

    def get_current_position():

        step = history[current_step]

        if step["position"] is not None:
            return step["position"]

        # Find the most recent ant position
        for previous_step in reversed(
            history[:current_step]
        ):

            if previous_step["position"] is not None:
                return previous_step["position"]

        return None

    # ==================================================
    # Draw Grid and Information
    # ==================================================

    def draw():

        ax.clear()

        step = history[current_step]

        position = get_current_position()

        # Draw grid
        ax.imshow(
            problem.grid,
            cmap="Greys",
            vmin=0,
            vmax=1
        )

        # Cell labels
        ax.set_xticks(range(problem.column))
        ax.set_yticks(range(problem.row))

        ax.set_xticklabels(range(problem.column))
        ax.set_yticklabels(range(problem.row))

        # Grid boundaries
        ax.set_xticks(
            np.arange(-0.5, problem.column, 1),
            minor=True
        )

        ax.set_yticks(
            np.arange(-0.5, problem.row, 1),
            minor=True
        )

        ax.grid(
            which="minor",
            color="black",
            linewidth=1
        )

        ax.tick_params(
            which="minor",
            bottom=False,
            left=False
        )

        # Start
        ax.scatter(
            problem.start[1],
            problem.start[0],
            color="lime",
            s=180,
            label="Start",
            edgecolors="black",
            zorder=8
        )

        # Destination
        ax.scatter(
            problem.dest[1],
            problem.dest[0],
            color="red",
            s=180,
            label="Destination",
            edgecolors="black",
            zorder=8
        )

        # Current ant path
        path = step["path"]

        if len(path) > 1:

            x = [p[1] for p in path]
            y = [p[0] for p in path]

            ax.plot(
                x,
                y,
                color="blue",
                linewidth=2,
                label="Ant path",
                zorder=7
            )

        # Best path
        best_path = step["best_path"]

        if best_path:

            x = [p[1] for p in best_path]
            y = [p[0] for p in best_path]

            ax.plot(
                x,
                y,
                color="lime",
                linestyle="--",
                linewidth=2,
                label="Best path",
                zorder=7
            )

        # Draw ant
        if position is not None:

            draw_ant(
                ax,
                position[0],
                position[1]
            )

        # Update pheromone panel
        draw_pheromones(
            pheromone_ax,
            step["pheromones"],
            position
        )

        # Title
        if step["ant"] is None:

            title = (
                f"Iteration: {step['iteration']} | "
                f"{step['status']}"
            )

        else:

            title = (
                f"Iteration: {step['iteration']} | "
                f"Ant: {step['ant']} | "
                f"Step: {current_step + 1}/{len(history)} | "
                f"{step['status']}"
            )

        ax.set_title(
            title,
            fontsize=12
        )

        ax.legend(
            loc="upper left",
            bbox_to_anchor=(1.02, 1)
        )

        ax.set_aspect("equal")

        fig.canvas.draw_idle()

    # ==================================================
    # Next Button
    # ==================================================

    def next_step(event):

        nonlocal current_step

        if current_step < len(history) - 1:

            current_step += 1
            draw()

    # ==================================================
    # Previous Button
    # ==================================================

    def previous_step(event):

        nonlocal current_step

        if current_step > 0:

            current_step -= 1
            draw()

    # ==================================================
    # Reset Button
    # ==================================================

    def reset(event):

        nonlocal current_step

        current_step = 0
        draw()

    # ==================================================
    # Buttons
    # ==================================================

    ax_previous = plt.axes(
        [0.25, 0.05, 0.15, 0.07]
    )

    ax_reset = plt.axes(
        [0.43, 0.05, 0.15, 0.07]
    )
    ax_next = plt.axes(
        [0.61, 0.05, 0.15, 0.07]
    )

    button_previous = Button(
        ax_previous,
        "Previous"
    )

    button_reset = Button(
        ax_reset,
        "Reset"
    )

    button_next = Button(
        ax_next,
        "Next"
    )

    button_previous.on_clicked(previous_step)
    button_reset.on_clicked(reset)
    button_next.on_clicked(next_step)

    # Initial display
    draw()

    plt.show()