CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre(
    id uuid PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role VARCHAR(255) NOT NULL,
    created timestamp with time zone,

    CONSTRAINT fk_person_id
        FOREIGN KEY (person_id)
        REFERENCES content.person (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_film_work_id
        FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id)
        ON DELETE CASCADE,

    CONSTRAINT uq_person_film_role
        UNIQUE (person_id, film_work_id, role)
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone,

    CONSTRAINT fk_genre_id
        FOREIGN KEY (genre_id)
        REFERENCES content.genre (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_film_work_id
        FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id)
        ON DELETE CASCADE,

    CONSTRAINT uk_genre_film
        UNIQUE (genre_id, film_work_id)
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work(creation_date);
CREATE INDEX IF NOT EXISTS film_work_title_idx ON content.film_work(title);
CREATE INDEX IF NOT EXISTS film_work_rating_idx ON content.film_work(rating);
CREATE INDEX IF NOT EXISTS genre_name_idx ON content.genre(name);
CREATE INDEX IF NOT EXISTS person_full_name_idx ON content.person(full_name);
