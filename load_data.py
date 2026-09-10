import csv
import sqlite3


def initialize_and_load():
    csv_file = "cell-count.csv"
    db_file = "cell_count.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS samples;
        DROP TABLE IF EXISTS subjects;

        CREATE TABLE subjects (
            subject TEXT PRIMARY KEY,
            project TEXT,
            condition TEXT,
            age INTEGER,
            sex TEXT,
            treatment TEXT,
            response TEXT,
            sample_type TEXT
        );

        CREATE TABLE samples (
            sample TEXT PRIMARY KEY,
            subject TEXT,
            time_from_treatment_start INTEGER,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER,
            FOREIGN KEY (subject) REFERENCES subjects(subject)
        );
    """)

    seen = set()
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            (
                project,
                subject,
                condition,
                age,
                sex,
                treatment,
                response,
                sample,
                sample_type,
                time_from_treatment_start,
                b_cell,
                cd8_t_cell,
                cd4_t_cell,
                nk_cell,
                monocyte,
            ) = row

            if subject not in seen:
                seen.add(subject)
                cursor.execute(
                    "INSERT INTO subjects VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (subject, project, condition, age, sex, treatment, response or None, sample_type),
                )

            cursor.execute(
                "INSERT INTO samples VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (sample, subject, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte),
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_and_load()
