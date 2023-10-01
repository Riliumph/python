CREATE TABLE sample_service.users (
    user_id serial NOT NULL PRIMARY KEY,
    user_name text NOT NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP
);
