CREATE TABLE TongueAnalysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    img_src VARCHAR(255),
    tongue_color INT,
    coating_color INT,
    tongue_thickness INT,
    rot_greasy INT, state INT,
    FOREIGN KEY (user_id) REFERENCES User(id)
)
