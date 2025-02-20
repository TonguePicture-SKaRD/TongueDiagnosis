CREATE TABLE chatRecord (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INT,
    content TEXT,
    create_at INT,
    role INT,
    FOREIGN KEY (session_id) REFERENCES chatSession(id)
);
