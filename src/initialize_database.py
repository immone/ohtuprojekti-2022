import os
import json
from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("drop table if exists value;")
    cursor.execute("drop table if exists reference;")
    cursor.execute("drop table if exists type_field;")
    cursor.execute("drop table if exists type;")
    cursor.execute("drop table if exists field;")

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        create table field (
            field_id integer not null,
            field_name text not null,
            unique (field_name),
            primary key (field_id)
        );
        """
    )

    cursor.execute(
        """
        create table type (
            type_id integer not null,
            type_name text not null,
            unique (type_name),
            primary key (type_id)
        );
        """
    )

    cursor.execute(
        """
        create table type_field (
            type_id integer,
            field_id integer,
            unique (type_id, field_id),
            foreign key (type_id) references type(type_id),
            foreign key (field_id) references field(field_id)
        );
        """
    )

    cursor.execute(
        """
    create table reference (
        reference_id text not null,
        type_id integer,
        unique (reference_id),
        foreign key (type_id) references type(type_id),
        primary key (reference_id)
    );
    """
    )

    cursor.execute(
        """
    create table value (
        reference_id text,
        field_id integer,
        value text default null,
        foreign key (reference_id) references reference(reference_id),
        foreign key (field_id) references field(field_id)
    );
    """
    )

    connection.commit()


def read_type_config():
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "..", "reference_type_config.json")) as file:
        return json.load(file)


def insert_types(connection, types: set):
    cursor = connection.cursor()

    for type_name in types:
        cursor.execute(
            "insert into type (type_name) values (?);", (type_name,))

    connection.commit()


def insert_fields(connection, fields: set):
    cursor = connection.cursor()

    for field_name in fields:
        cursor.execute(
            "insert into field (field_name) values (?);", (field_name,))

    connection.commit()


def insert_reference_types(connection):
    reference_types = read_type_config()
    cursor = connection.cursor()

    insert_types(connection, set(reference_types.keys()))
    insert_fields(connection, set(
        field for fields in reference_types.values() for field in fields))
    for type_name, fields in reference_types.items():
        for field in fields:
            cursor.execute(
                """
                insert into type_field (type_id, field_id)
                values (
                    (select type_id from type where type_name = ?),
                    (select field_id from field where field_name = ?)
                );
                """,
                (type_name, field)
            )

    connection.commit()


def initialize_database():

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)
    insert_reference_types(connection)
