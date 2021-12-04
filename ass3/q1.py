# COMP3311 19T3 Assignment 3

import cs3311
import psycopg2
conn = cs3311.connect()

cur = conn.cursor()

query = """ 
select s.code, c.quota, count(p.id)
from Subjects s 
join Courses c on (s.id = c.subject_id)
join Terms t on (c.term_id = t.id)
join Course_Enrolments ce on (ce.course_id = c.id)
join People p on (p.id = ce.person_id)
where c.quota > 50 and t.name = '19T3'
group by s.code, c.quota
order by s.code asc
"""

cur.execute(query)
for item in cur.fetchall():
    if (item[2] > item[1]):
        percentage = (item[2]/item[1]) * 100
        print (item[0] + " " + str(round(percentage)) + "%")

cur.close()
conn.close()
