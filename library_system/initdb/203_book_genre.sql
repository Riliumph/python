CREATE TABLE
    lib_sys.books_genres (
        id serial PRIMARY KEY,
        book_id INT NOT NULL,
        genre_id INT NOT NULL,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (book_id) REFERENCES lib_sys.books (book_id),
        FOREIGN KEY (genre_id) REFERENCES lib_sys.genres (genre_id),
        UNIQUE (book_id, genre_id)
    );

INSERT INTO
    lib_sys.books_genres (book_id, genre_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 3),
    (3, 4),
    (4, 3);
