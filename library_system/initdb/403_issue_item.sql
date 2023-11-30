CREATE TABLE
    lib_sys.issue_items (
        user_id INT,
        inventory_id INT,
        issue_date timestamptz,
        due_date timestamptz,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES lib_sys.users (user_id),
        FOREIGN KEY (inventory_id) REFERENCES lib_sys.inventories (inventory_id)
    );

INSERT INTO
    lib_sys.issue_items (user_id, inventory_id, issue_date, due_date)
VALUES
    (1, 1, '2020-01-06', '2020-01-20'),
    (2, 2, '2020-01-06', '2020-01-20'),
    (3, 2, '2020-01-06', '2020-01-20'),
    (1, 4, '2020-01-06', '2020-01-20');
