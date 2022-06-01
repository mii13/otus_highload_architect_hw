create table message
(
    id         int auto_increment,
    chat_id    int      not null,
    text       text     not null,
    created_at datetime not null,
    user_id    int      not null,
    constraint message_pk primary key (id)
);