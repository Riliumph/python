CREATE TABLE
    lib_sys.issue_histories (
        checkout_history_id serial PRIMARY KEY,
        user_id INT,
        inventory_id INT,
        issue_date timestamptz,
        return_date timestamptz,
        created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES lib_sys.users (user_id),
        FOREIGN KEY (inventory_id) REFERENCES lib_sys.inventories (inventory_id)
    );

INSERT INTO
    lib_sys.issue_histories (user_id, inventory_id, issue_date, return_date)
VALUES
    (2, 2, '2020-01-05', '2020-01-15');
