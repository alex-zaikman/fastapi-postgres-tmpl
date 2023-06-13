
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  scopes TEXT[] NOT NULL
);


GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;

INSERT INTO users (email, password, scopes)
VALUES ('alex@gmail.com', '$2b$12$anLRbqyOV9YvC49qggeDHOEUCwZDZlsPhBelD/iaEn4uVUhUfZGmC', ARRAY ['USER']),
       ('admin@gmail.com', '$2b$12$S9ES4ywuyPkYfzwTMwmC3.Pqs82FCJ.iqiAASzcWul8qK4LG94ZD6', ARRAY ['ADMIN']);