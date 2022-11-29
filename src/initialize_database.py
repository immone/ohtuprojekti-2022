from database_connection import get_database_connection


def drop_tables(connection):

    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists reference;
    """)

    cursor.execute("""
        drop table if exists reference_author;
    """)

    cursor.execute("""
        drop table if exists author;
    """)

    connection.commit()


def create_tables(connection):

    cursor = connection.cursor()

    cursor.execute("""
        create table author (
            author_id integer not null,
            name text not null,
            unique (name),
            primary key (author_id)
        );
    """)

    cursor.execute("""
        create table reference (
            reference_id text not null,
            title text not null,
            year integer not null,
            publisher text not null,
            primary key (reference_id)
        );
    """)

    cursor.execute("""
         create table reference_author (
            reference_id text,
            author_id integer,
            foreign key (reference_id) references reference(reference_id),
            foreign key (author_id) references author(author_id)
        );
    """)

    connection.commit()


def initialize_database():

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)
