CREATE TABLE chatRecord (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INT,
    content TEXT,
    create_at DATETIME,
    role INT,
    FOREIGN KEY (session_id) REFERENCES chatSession(id)
);
