CREATE TABLE
    lib_sys.inventories (
        inventory_id serial PRIMARY KEY,
        book_id INT,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (book_id) REFERENCES lib_sys.books (book_id)
    );

INSERT INTO
    lib_sys.inventories (book_id)
VALUES
    (1),
    (2),
    (3),
    (4),
    (2);
