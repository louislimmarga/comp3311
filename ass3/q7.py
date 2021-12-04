# COMP3311 19T3 Assignment 3

import cs3311
import psycopg2
import sys
conn = cs3311.connect()

cur = conn.cursor()

code = '19T1'
if len(sys.argv) > 1 :
    code = sys.argv[1]

query = """
select r.id, m.day, m.start_time, m.end_time, m.weeks_binary, t.name
from Subjects s 
join Courses c on (s.id = c.subject_id)
join Terms t on (c.term_id = t.id)
join Classes cl on (cl.course_id = c.id)
join Meetings m on (m.class_id = cl.id)
join Rooms r on (r.id = m.room_id)
where substr(r.code, 1, 2) = 'K-'
group by r.id, m.day, m.start_time, m.end_time, m.weeks_binary, t.name
order by r.id asc, m.day asc, m.start_time asc, m.end_time desc, m.weeks_binary asc
"""

query2 = """
select count(*)
from Rooms r
where substr(r.code, 1, 2) = 'K-'
"""
cur.execute(query)
first = 0
under = 0
total = 0
prev = cur.fetchone()
totalroom = 0
for x in cur.fetchall():
    if x[5] != code:
        continue
    if int(x[0]) != int(prev[0]):
        first = 0
        
        if total / 1000 < 20:
            under = under + 1
            with open("dd.txt", "a") as f:
                f.write(str(prev[0]) + " under\n")
        else:
            with open("dd.txt", "a") as f:
                f.write(str(prev[0]) + " ok\n")
            
        totalroom = totalroom + 1
        
        total = 0
    
    if (x[0]-prev[0]) != 1 and (x[0]-prev[0]) != 0:
        for i in range(1, x[0]-prev[0]):
            with open("dd.txt", "a") as f:
                f.write(str(i + prev[0]) + " under\n")

    if first == 0:
        for i in range(0,10):
            if x[4][i] == "1":
                first = x[3]
                second = x[2]
                if int(x[3]) % 100 != 0:
                    first = x[3] + 20
                if int(x[2]) % 100 != 0:
                    second = x[2] + 20
                total = total + first - second
        first = 1
        prev = x
        continue
    
    for i in range(0,10):
        if x[4][i] == "1":
            first = x[3]
            second = x[2]
            if int(x[3]) % 100 != 0:
                first = x[3] + 20
            if int(x[2]) % 100 != 0:
                second = x[2] + 20
            total = total + first - second
    prev = x
    

cur.execute(query2)
total = cur.fetchone()[0]

under = under + total - totalroom

print(under)
output = int(under) / int(total) * 100
print(str(round(output, 1)) + "%")
cur.close()
conn.close()
