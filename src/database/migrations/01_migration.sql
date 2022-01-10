create table IF NOT EXISTS user
(
    id INT NOT NULL AUTO_INCREMENT,
    email varchar(200) not null unique,
	name varchar(100) not null,
    second_name varchar(100) not null,
    age int not null,
    gender char(1) not null,
    interests text not null,
    city varchar(200) not null,
    created_at datetime default now() not null,
    password varchar(255),
    CONSTRAINT id PRIMARY KEY (id)
);

create table IF NOT EXISTS token
(
    id INT NOT NULL AUTO_INCREMENT,
    token varchar(255) not null,
    created_at datetime default now() not null,
    CONSTRAINT id PRIMARY KEY (id)
);
