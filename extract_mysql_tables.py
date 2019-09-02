#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command-line utility for extracting data from a MySQL database and
writing each table to a file with tab-separated values. Each file will
be named after the table, suffixed with ".tsv".
"""

import argparse
import csv
import getpass
import os
import sys

import pymysql


__author__ = 'Markus Englund'
__license__ = 'MIT'
__version__ = '0.1.0'


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = parse_args(args)

    if not parser.password:
        password = getpass.getpass('MySQL password:')
    else:
        password = parser.password

    mysql_connection = pymysql.connect(
        host=parser.host, user=parser.user, password=password,
        db=parser.database, charset='utf8')

    try:
        if parser.tablefile_filepath is None:
            table_list = list_all_tables(mysql_connection, parser.table_type)
        else:
            table_list = read_file_into_list(parser.tablefile_filepath)

        for table_name in table_list:
            print('Exporting table: ' + table_name)
            output_filepath = os.path.join(
                parser.output_dirpath, table_name + '.tsv')
            table_to_tsv(mysql_connection, table_name, output_filepath)
    finally:
        mysql_connection.close()


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='extract_mysql_tables.py', description=(
            'Command-line utility for exporting tables from a MySQL '
            'database to files in tab-separated values (TSV) format.'))
    parser.add_argument(
        '-V', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument(
        '-u', '--user', type=str, action='store', default='root',
        dest='user', help='MySQL user (default: "root")')
    parser.add_argument(
        '-p', '--password', type=str, action='store', default=None,
        dest='password', help='MySQL password')
    parser.add_argument(
        '--host', type=str, action='store', default='localhost',
        dest='host', help='database host (default: "localhost")')
    parser.add_argument('database', action='store', help='database name')
    parser.add_argument(
        '--table-type', type=int, action=StoreTableTypeName,
        choices=range(1, 4), default=None, help=(
            'Table type to include in export: 1=BASE TABLE; 2=VIEW; '
            '3=SYSTEM VIEW (i.e. INFORMATION_SCHEMA table). The table type '
            'will be ignored if there is a file provided with table names.'))
    parser.add_argument(
        '-o', '--output-dir', dest='output_dirpath', type=is_directory,
        action=StoreExpandedPath, default=os.getcwd(), metavar='DIR',
        help='path to the output directory (default: current directory)')
    parser.add_argument(
        'tablefile_filepath', metavar='table-file', action=StoreExpandedPath,
        type=is_file, nargs='?', default=None, help=(
            'file with table names separated by newline characters '
            '(if missing, all tables will be exported)'))
    return parser.parse_args(args)


class StoreExpandedPath(argparse.Action):
    """Invoke shell-like path expansion for user- and relative paths."""

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            filepath = os.path.abspath(os.path.expanduser(str(values)))
            setattr(namespace, self.dest, filepath)


class StoreTableTypeName(argparse.Action):
    """Store the table type name based on a given integer."""

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            d = dict(zip(range(1, 4), ['BASE TABLE', 'VIEW', 'SYSTEM VIEW']))
            table_type = d[values]
            setattr(namespace, self.dest, table_type)


def table_to_tsv(conn, table_name, output_filepath):
    """Export table to a TSV file."""
    cursor = conn.cursor()
    cursor.execute('select * from ' + table_name + ';')
    with open(output_filepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t')
        csv_writer.writerow([i[0] for i in cursor.description])  # headers
        csv_writer.writerows(cursor)


def is_directory(dirname):
    """Check if a path is a directory."""
    if not os.path.isdir(dirname):
        msg = '{0} is not a directory'.format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def is_file(filename):
    """Check if a path is a file."""
    if not os.path.isfile(filename):
        msg = '{0} is not a file'.format(filename)
        raise argparse.ArgumentTypeError(msg)
    else:
        return filename


def list_all_tables(conn, table_type=None):
    """Return a list with names of all tables in the database."""
    if table_type is not None:
        sql_query = (
            "show full tables where TABLE_TYPE = '{}';"
            .format(table_type))
    else:
        sql_query = 'show full tables;'
    cursor = conn.cursor()
    cursor.execute(sql_query)
    return [name for (name, _) in cursor]


def read_file_into_list(filepath):
    """Read file into a list of strings while dropping empty lines."""
    with open(filepath) as f:
        lst = []
        for line in f:
            stripped_line = line.strip()
            if stripped_line:
                lst.append(stripped_line)
    return lst


if __name__ == '__main__':
    main()
