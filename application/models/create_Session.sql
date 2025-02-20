CREATE TABLE chatSession (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    tittle text,
    FOREIGN KEY (user_id) REFERENCES User(id)
);
