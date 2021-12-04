# COMP3311 19T3 Assignment 3

import cs3311
import psycopg2
import sys
conn = cs3311.connect()

cur = conn.cursor()

incommon = 2
if len(sys.argv) > 1 :
    incommon = sys.argv[1]

query = """
select substr(s.code, 5) as sub, count(*) as total, string_agg(substr(s.code, 1, 4), ' ' order by s.code)
from Subjects s
group by substr(s.code, 5) having count(*) > 1
order by count(*), substr(s.code, 5)
"""

cur.execute(query)

for item in cur.fetchall():
    if int(item[1]) == int(incommon):
        print(item[0] + ": " + item[2])

cur.close()
conn.close()
