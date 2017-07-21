# -*- coding: utf-8 -*-

import psycopg2


print("Logs Analysis Project - by Jonathan Machado")
print("")

# Database connection
conn = psycopg2.connect("dbname='news'")
cur = conn.cursor()

# Question 1. What are the most popular three articles of all time?
print("1. What are the most popular three articles of all time?")
print("")
cur.execute(
    """select a.title,l.path, a.author, count(*) as views
    FROM log l
    INNER JOIN articles a on (replace(path, '/article/', '') = a.slug)
    GROUP BY l.path, a.title, a.author
    ORDER BY views desc
    LIMIT 3;""")
rows = cur.fetchall()

for row in rows:
    print ('"%s" — %s views' % (row[0], row[3]))
    # Example: "Princess Shellfish Marries Prince Handsome" — 1201 views
print("")

# Question 2. Who are the most popular article authors of all time?
print("2. Who are the most popular article authors of all time?")
print("")

cur.execute(
    """select authors.name, sum (views) as total_views
    from (
        select a.title,l.path, a.author, count(*) as views
        from log l
        inner join articles a on (replace(path, '/article/', '') = a.slug)
        group by l.path, a.title, a.author
        order by views desc) as sub
    join authors on sub.author = authors.id
    group by name
    order by total_views desc;""")
rows = cur.fetchall()
for row in rows:
    print ('%s — %s views' % (row[0], row[1]))
    # Example: Ursula La Multa — 2304 views
print("")

# Question 3
print("3. On which days did more than 1% of requests lead to errors?")
print("")

cur.execute(
    """
    SELECT to_char(sub.time, 'Month DD, YYYY'), total_requests,
        count(*) as total_404, count(*) / total_requests::float *100 as percent
    FROM (
        SELECT time::date, count(*) as total_requests
        FROM log group by time::date) as sub
    JOIN log on (sub.time = log.time::date)
    WHERE log.status = '404 NOT FOUND'
    GROUP BY log.time::date, sub.time, total_requests
    HAVING count(*) > (total_requests * 0.01);""")
rows = cur.fetchall()
for row in rows:
    print("{0} — {1:.2f}".format(row[0], row[3]))
    # Example: July 29, 2016 — 2.5% errors
print("")

conn.close()
