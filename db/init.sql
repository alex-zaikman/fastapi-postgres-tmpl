create sequence public.user_id_seq;

alter sequence public.user_id_seq owner to postgres;

create table public.users (
  id integer primary key not null,
  email character varying,
  password character varying,
  scopes character varying[]
);

INSERT INTO public.users (id, email, password, scopes)
VALUES (nextval('user_id_seq'),'alex@gmail.com', '$2b$12$anLRbqyOV9YvC49qggeDHOEUCwZDZlsPhBelD/iaEn4uVUhUfZGmC', ARRAY ['USER']),
       (nextval('user_id_seq'),'admin@gmail.com', '$2b$12$S9ES4ywuyPkYfzwTMwmC3.Pqs82FCJ.iqiAASzcWul8qK4LG94ZD6', ARRAY ['ADMIN']);
