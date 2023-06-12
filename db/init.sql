
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  scopes TEXT[] NOT NULL
);

INSERT INTO users (email, password, scopes)
VALUES ('alex@gmail.com', '$2b$12$anLRbqyOV9YvC49qggeDHOEUCwZDZlsPhBelD/iaEn4uVUhUfZGmC', ARRAY ['USER']);