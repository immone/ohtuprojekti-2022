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
        drop table if exists reference_tag;
    """)

    cursor.execute("""
        drop table if exists author;
    """)

    cursor.execute("""
        drop table if exists tag;
    """)

    connection.commit()


def create_tables(connection):

    cursor = connection.cursor()

    cursor.execute(
    """
    create table author (
        author_id integer not null,
        name text not null,
        unique (name),
        primary key (author_id)
    );
    """
    )

    cursor.execute(
    """
    create table tag (
        tag_id integer not null,
        name text not null,
        unique (name),
        primary key (tag_id)
    );
    """
    )

    cursor.execute(
    """
    create table reference (
        reference_id text not null,
        title text not null,
        year integer not null,
        publisher text not null,
        primary key (reference_id)
    );
    """
    )

    cursor.execute(
    """
    create table reference_author (
        reference_id text,
        author_id integer,
        unique (reference_id, author_id),
        foreign key (reference_id) references reference(reference_id),
        foreign key (author_id) references author(author_id)
    );
    """
    )

    cursor.execute(
    """
    create table reference_tag (
        reference_id text,
        tag_id integer,
        unique (reference_id, tag_id),
        foreign key (reference_id) references reference(reference_id),
        foreign key (tag_id) references tag(tag_id)
    );
    """
    )


    connection.commit()


def initialize_database():

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)
