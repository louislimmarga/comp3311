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
select substr(s.code, 1, 4) as sub, string_agg(b.name, '-'), string_agg(substr(s.code, 5), '-')
from Subjects s 
join Courses c on (s.id = c.subject_id)
join Terms t on (c.term_id = t.id)
join Classes cl on (cl.course_id = c.id)
join Meetings m on (m.class_id = cl.id)
join Rooms r on (r.id = m.room_id)
join Buildings b on (b.id = r.within)
where t.name = '19T2'
group by substr(s.code, 1, 4)
order by substr(s.code, 1, 4)
"""

cur.execute(query)
buildings = []
num = []
for item in cur.fetchall():
    if item[0] == code:
        buildings = item[1].split("-")
        num = item[2].split("-")
        break

d = {}
for x, y in zip(buildings, num):
    d.setdefault(x, []).append(y)


d = sorted(d.items())

for x, y in d:
    y.sort()

i = 0
prevb = None
for x, z in d:
    prevn = None
    if prevb != x:
        print(x)
        prevb = x
    for y in z:
        if y == prevn:
            continue
        print(" "+code+y)
        prevn = y
    


cur.close()
conn.close()
