BEGIN;
CREATE TABLE "forums_subforum" (
    "id" integer NOT NULL PRIMARY KEY,
    "parent_id" integer,
    "title" varchar(200) NOT NULL,
    "description" varchar(200) NOT NULL
)
;
CREATE TABLE "forums_thread" (
    "id" integer NOT NULL PRIMARY KEY,
    "subforum_id" integer NOT NULL REFERENCES "forums_subforum" ("id"),
    "creator_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "title" varchar(200) NOT NULL,
    "creation_date" datetime NOT NULL,
    "sticky" bool NOT NULL
)
;
CREATE TABLE "forums_post" (
    "id" integer NOT NULL PRIMARY KEY,
    "thread_id" integer NOT NULL REFERENCES "forums_thread" ("id"),
    "poster_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "title" varchar(200) NOT NULL,
    "content" text NOT NULL,
    "is_op" bool NOT NULL,
    "pub_date" datetime NOT NULL
)
;

CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "password" varchar(128) NOT NULL,
    "last_login" datetime NOT NULL,
    "is_superuser" bool NOT NULL,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "date_joined" datetime NOT NULL
)
;

COMMIT;
