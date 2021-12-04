# COMP3311 19T3 Assignment 3

import cs3311
import psycopg2
import sys
conn = cs3311.connect()

cur = conn.cursor()

def update(week):
    binary = ["0","0","0","0","0","0","0","0","0","0","0"]
    if "<" in week or "N" in week:
        str1 = ""
        binary = str1.join(binary)
        with open("ccccc.txt", "a") as f:
            return binary
    
    week = week.split(",")
    for x in week:
        if "-" in x:
            x = x.split("-")
            for i in range(int(x[0]), int(x[1]) + 1):
                binary[i - 1] = "1"
        else:
            a = int(x) - 1
            binary[a] = "1"
    str1 = ""
    binary = str1.join(binary) 
    return binary

query = """
select m.id, weeks
from Meetings m
order by m.id
"""

cur.execute(query)

for item in cur.fetchall():
    week = item[1]
    binary = update(week)
    query1 = ("UPDATE meetings SET weeks_binary = '{}' WHERE id = {};\n".format(binary, item[0]))
    cur.execute(query1)
    
cur.close()
conn.commit()
conn.close()
