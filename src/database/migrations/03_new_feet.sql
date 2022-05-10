create table IF NOT EXISTS post
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    text text NOT NULL,
    created_at datetime default now() not null,
    FOREIGN KEY (user_id) REFERENCES user (id)
);