CREATE TABLE
    lib_sys.users (
        user_id serial PRIMARY KEY,
        user_name TEXT NOT NULL,
        age INT NOT NULL,
        wage DECIMAL NOT NULL,
        enrollment_day timestamptz DEFAULT CURRENT_TIMESTAMP,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    lib_sys.users (user_name, age, wage)
VALUES
    ('渋谷ユウト', 13, 1.0),
    ('大崎トシコ', 12, 1.0),
    ('大塚ミチオ', 22, 1.0),
    ('品川マコト', 30, 1.0);
