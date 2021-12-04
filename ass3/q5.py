# COMP3311 19T3 Assignment 3

import cs3311
import psycopg2
import sys
conn = cs3311.connect()

cur = conn.cursor()

course = 'COMP1521'
if len(sys.argv) > 1 :
    course = sys.argv[1]

query = """
select s.code, ct.name, cl.quota, cl.tag, count(distinct p.id)
from Subjects s 
join Courses c on (s.id = c.subject_id)
join Terms t on (c.term_id = t.id)
join Course_Enrolments ce on (ce.course_id = c.id)
join People p on (p.id = ce.person_id)
join Classes cl on (cl.course_id = c.id)
join ClassTypes ct on (ct.id = cl.type_id)
join Class_Enrolments cle on (cle.class_id = cl.id and cle.person_id = p.id)
where t.name = '19T3'
group by s.code, cl.quota, ct.name, cl.tag
order by ct.name asc
"""

cur.execute(query)
prev = None
for item in cur.fetchall():
    if item[0] == course and item[4]/item[2] < 0.5:
        percentage = (item[4]/item[2]) * 100
        print(item[1] + " " + item[3] + " is " + str(round(percentage)) +"% full")

cur.close()
conn.close()