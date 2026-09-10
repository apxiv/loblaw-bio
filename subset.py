import sqlite3


def analyze_subset():
    conn = sqlite3.connect("cell_count.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS subset_samples")
    cursor.execute("""
        CREATE TABLE subset_samples AS
        SELECT sa.sample, s.subject, s.project, s.response, s.sex
        FROM samples sa
        JOIN subjects s ON s.subject = sa.subject
        WHERE s.condition = 'melanoma'
          AND s.sample_type = 'PBMC'
          AND s.treatment = 'miraclib'
          AND sa.time_from_treatment_start = 0
    """)

    cursor.execute("DROP TABLE IF EXISTS subset_counts")
    cursor.execute("""
        CREATE TABLE subset_counts (
            question TEXT,
            category TEXT,
            n INTEGER
        )
    """)

    cursor.execute("""
        INSERT INTO subset_counts
        SELECT 'samples_per_project', project, COUNT(*)
        FROM subset_samples
        GROUP BY project
    """)
    cursor.execute("""
        INSERT INTO subset_counts
        SELECT 'subjects_by_response', response, COUNT(DISTINCT subject)
        FROM subset_samples
        GROUP BY response
    """)
    cursor.execute("""
        INSERT INTO subset_counts
        SELECT 'subjects_by_sex', sex, COUNT(DISTINCT subject)
        FROM subset_samples
        GROUP BY sex
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    analyze_subset()
