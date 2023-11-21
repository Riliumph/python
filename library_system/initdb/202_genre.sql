CREATE TABLE
    lib_sys.genres (
        genre_id serial PRIMARY KEY,
        genre_name TEXT NOT NULL,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    lib_sys.genres (genre_name)
VALUES
    ('IT'),
    ('データベース'),
    ('SF'),
    ('ラブストーリー');
