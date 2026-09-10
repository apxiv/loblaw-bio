import sqlite3


def summarize_frequencies():
    conn = sqlite3.connect("cell_count.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS population_frequencies")
    cursor.execute("""
        CREATE TABLE population_frequencies (
            sample TEXT,
            total_count INTEGER,
            population TEXT,
            count INTEGER,
            percentage REAL
        )
    """)

    cursor.execute(
        "SELECT sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte FROM samples"
    )

    rows = []
    for sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte in cursor.fetchall():
        total_count = b_cell + cd8_t_cell + cd4_t_cell + nk_cell + monocyte
        for population, count in (
            ("b_cell", b_cell),
            ("cd8_t_cell", cd8_t_cell),
            ("cd4_t_cell", cd4_t_cell),
            ("nk_cell", nk_cell),
            ("monocyte", monocyte),
        ):
            percentage = 100 * count / total_count
            rows.append((sample, total_count, population, count, percentage))

    cursor.executemany(
        "INSERT INTO population_frequencies VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    summarize_frequencies()
