import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu


def compare_response():
    conn = sqlite3.connect("cell_count.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS response_comparison")
    cursor.execute("""
        CREATE TABLE response_comparison (
            population TEXT,
            p_value REAL
        )
    """)

    populations = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
    fig, axes = plt.subplots(1, 5, figsize=(16, 4))

    for ax, population in zip(axes, populations):
        rows = cursor.execute(
            """
            SELECT pf.percentage, s.response
            FROM population_frequencies pf
            JOIN samples sa ON sa.sample = pf.sample
            JOIN subjects s ON s.subject = sa.subject
            WHERE s.condition = 'melanoma'
              AND s.treatment = 'miraclib'
              AND s.sample_type = 'PBMC'
              AND pf.population = ?
            """,
            (population,),
        ).fetchall()

        yes = [percentage for percentage, response in rows if response == "yes"]
        no = [percentage for percentage, response in rows if response == "no"]

        _, p_value = mannwhitneyu(yes, no)
        cursor.execute(
            "INSERT INTO response_comparison VALUES (?, ?)",
            (population, p_value),
        )

        ax.boxplot([no, yes], tick_labels=["non-responder", "responder"])
        ax.set_title(population)
        ax.set_ylabel("% of cells")

    conn.commit()
    conn.close()

    plt.tight_layout()
    plt.savefig("response_boxplots.png")
    plt.close()


if __name__ == "__main__":
    compare_response()
