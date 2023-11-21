CREATE TABLE
    lib_sys.users (
        user_id serial PRIMARY KEY,
        user_name TEXT NOT NULL,
        age INT NOT NULL,
        enrollment_day timestamptz DEFAULT CURRENT_TIMESTAMP,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    lib_sys.users (user_name, age)
VALUES
    ('渋谷ユウト', 13),
    ('大崎トシコ', 12),
    ('大塚ミチオ', 22),
    ('品川マコト', 30);
