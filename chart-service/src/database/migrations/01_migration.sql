create table chat
(
    id         int auto_increment,
    name    varchar(100)     not null,
    created_at datetime not null,
    constraint chat_pk primary key (id)
);

create table participant
(
    id         int auto_increment,
    chat_id    int      not null,
    user_id    int      not null,
    last_read_message int not null default 0,
    constraint participant_pk primary key (id),
    FOREIGN KEY (chat_id) REFERENCES chat (id)

);

