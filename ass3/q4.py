# COMP3311 19T3 Assignment 3

import cs3311
import psycopg2
import sys
conn = cs3311.connect()

cur = conn.cursor()

code = 'ENGG'
if len(sys.argv) > 1 :
    code = sys.argv[1]

query = """
select s.code, t.name, count(p.id)
from Subjects s 
join Courses c on (s.id = c.subject_id)
join Terms t on (c.term_id = t.id)
join Course_Enrolments ce on (ce.course_id = c.id)
join People p on (p.id = ce.person_id)
group by s.code, t.name
order by t.name asc, substr(s.code, 5) asc
"""

cur.execute(query)
prev = None
for item in cur.fetchall():
    false = 0
    for i in range(0,3):
        if item[0][i] != code[i]:
            false = 1
    if false == 1:
        continue
    if item[1] != prev:
            print(item[1])
    prev = item[1]
    print(" "+item[0]+"("+str(item[2])+")")
        
cur.close()
conn.close()
