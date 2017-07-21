#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
        as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """
    conn = psycopg2.connect("dbname='news'")
    cur = conn.cursor()
    return conn, cur


def execute_query(query):
    """execute_query takes an SQL query as a parameter.
        Executes the query and returns the results as a list of tuples.
       args:
           query - an SQL query statement to be executed.

       returns:
           A list of tuples containing the results of the query.
           :param query: a SQL query to be executed on the database by the function.
    """
    conn, cur = db_connect()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def print_top_articles():
    """Prints out the top 3 articles of all time."""

    query = """
    SELECT a.title, count(*) AS views
    FROM log l
    INNER JOIN articles a ON (path = '/article/' || a.slug)
    GROUP BY a.title
    ORDER BY views DESC
    LIMIT 3;
    """
    results = execute_query(query)
    # Question 1. What are the most popular three articles of all time?
    print("1. What are the most popular three articles of all time?")
    print("")

    for title, views in results:
        # print('"%s" — %s views' % (title, views))
        print("\"{}\" — {} views".format(title, views))
        # Example: "Princess Shellfish Marries Prince Handsome" — 1201 views
    print("")


def print_top_authors():
    """Prints a list of authors ranked by article views."""

    query = """
    SELECT authors.name, views
    FROM (
        SELECT a.author, count(*) AS views
        FROM log l
        INNER JOIN articles a ON (path = '/article/' || a.slug)
        GROUP BY a.author
        ORDER BY views DESC) AS sub
    JOIN authors ON sub.author = authors.id;
    """
    results = execute_query(query)
    # Question 2. Who are the most popular article authors of all time?
    print("2. Who are the most popular article authors of all time?")
    print("")

    for author, views in results:
        print('%s — %s views' % (author, views))
        # Example: Ursula La Multa — 2304 views
    print("")


def print_errors_over_one():
    """Prints out the days where more than 1% of logged access requests were errors."""

    query = """
    SELECT to_char(sub.time, 'FMMonth DD, YYYY'), total_requests,
        count(*) as total_404, count(*) / total_requests::float *100 as percent
    FROM (
        SELECT time::date, count(*) as total_requests
        FROM log group by time::date) as sub
    JOIN log on (sub.time = log.time::date)
    WHERE log.status = '404 NOT FOUND'
    GROUP BY log.time::date, sub.time, total_requests
    HAVING count(*) > (total_requests * 0.01);
    """
    results = execute_query(query)
    # Question 3
    print("3. On which days did more than 1% of requests lead to errors?")
    print("")

    for row in results:
        print("{0} — {1:.2f}% errors".format(row[0], row[3]))
        # Example: July 29, 2016 — 2.5% errors
    print("")


if __name__ == '__main__':
    print("Logs Analysis Project - by Jonathan Machado")
    print("")
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
