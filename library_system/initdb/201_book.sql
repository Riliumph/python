CREATE TABLE
    lib_sys.books (
        book_id serial PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publisher TEXT NOT NULL,
        publication_date timestamptz,
        pages INT NOT NULL,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    lib_sys.books (title, author, publisher, publication_date, pages)
VALUES
    ('わたしとぼくのPL/pgSQL', '目黒聖', 'インプレスR&D', '2019-02-22', 10),
    ('あるマグロの一生', '目黒聖', 'めぐろ社', '2010-04-19', 300),
    ('マグロの生態', '目黒聖', 'めぐろ社', '2015-08-01', 500),
    ('マグロの歴史', '目黒聖', 'めぐろ社', '2017-01-19', 230);
