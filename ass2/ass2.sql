-- COMP3311 19T3 Assignment 2
-- Written by <<insert your name here>>

-- Q1 Which movies are more than 6 hours long? 

create or replace view Q1(title)
as
    select   t.main_title as title 
    from     Titles t 
    where    t.runtime > 360 and t.format = 'movie' order by t.main_title asc;
;


-- Q2 What different formats are there in Titles, and how many of each?

create or replace view Q2(format, ntitles)
as
    select   t.format as format, count(*) as ntitles
    from     Titles t
    group by t.format
;


-- Q3 What are the top 10 movies that received more than 1000 votes?

create or replace view Q3(title, rating, nvotes)
as
    select   t.main_title as title, t.rating as rating, t.nvotes
    from     Titles t
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


-- Q4 What are the top-rating TV series and how many episodes did each have?

create or replace view Q4(title, nepisodes)
as
    select   t.main_title as title, count(e.episode) as nepisodes
    from     Titles t join Episodes e on (t.id = e.parent_id)
    where    (t.format = 'tvSeries' or t.format = 'tvMiniSeries') and
             rating = 10
    group by t.main_title
;


-- Q5 Which movie was released in the most languages?

create or replace view Q5(title, nlanguages)
as
    select   t.main_title as title, count(distinct a.language) as nlanguages
    from     Titles t join Aliases a on (t.id = a.title_id)
    where    t.format = 'movie' and a.language is not null
    group by t.main_title
    having   count(distinct a.language) = 
                (select max(b.total)
                 from (select count(distinct a.language) as total
                    from Titles t join Aliases a on (t.id = a.title_id)  
                    where    t.format = 'movie' and a.language is not null     
                    group by t.main_title) as b)
;

-- Q6 Which actor has the highest average rating in movies that they're known for?

create or replace view Q6(name)
as
    select  name
    from    (select n.name, avg(t.rating) as avg_rating
    from     Names n 
        inner join Known_for k on (k.name_id = n.id)
        inner join Titles t on (t.id = k.title_id)
        join Worked_as w on (w.name_id = n.id)
    where    w.work_role = 'actor' and t.format = 'movie' and t.rating is not null
    group by n.name
    having   count(t.rating) > 1
    ) as findavgrating
    where avg_rating = (select max(avg_rating)
        from    (select n.name, avg(t.rating) as avg_rating
        from     Names n 
            inner join Known_for k on (k.name_id = n.id)
            inner join Titles t on (t.id = k.title_id)
            join Worked_as w on (w.name_id = n.id)
        where    w.work_role = 'actor' and t.format = 'movie' and t.rating is not null
        group by n.name
        having   count(t.rating) > 1
        )as findmaxrating) ;

-- Q7 For each movie with more than 3 genres, show the movie title and a comma-separated list of the genres


create or replace view Q7(title,genres)
as
    select   t.main_title as title, string_agg(g.genre, ',' order by g.genre)
    from     Titles t
        join Title_genres g on (t.id = g.title_id)
    where    t.format = 'movie'
    group by t.id
    having   count(t.main_title) > 3
    order by t.main_title asc
;

-- Q8 Get the names of all people who had both actor and crew roles on the same movie

create or replace view Q8(name)
as    
    select   distinct n.name
    from     Titles t
        join Actor_roles ar on (t.id = ar.title_id)
        join Crew_roles cr on (t.id = cr.title_id)
        join Names n on (ar.name_id = n.id and cr.name_id = n.id)  
    where    t.format = 'movie'
    order by n.name asc  
;

-- Q9 Who was the youngest person to have an acting role in a movie, and how old were they when the movie started?

create or replace view Q9(name,age)
as
    select   n.name as name, min(t.start_year - n.birth_year) as age
    from     Actor_roles  r
        join Titles t on (t.id = r.title_id)
        join Names n on (r.name_id = n.id)
    where    t.format = 'movie'
    group by n.name
    having   min(t.start_year-n.birth_year) = 
                (select min(b.total)
                from(select   min(t.start_year - n.birth_year) as total
                    from     Actor_roles  r
                        join Titles t on (t.id = r.title_id)
                        join Names n on (r.name_id = n.id)
                    where    t.format = 'movie'
                    group by n.name) as b)
;

-- Q10 Write a PLpgSQL function that, given part of a title, shows the full title and the total size of the cast and crew

create or replace function
	Q10(partial_title text) returns setof text
as $$
declare
    _title Titles;
    _crew Crew_roles;
    _actor Actor_roles;
    _prin Principals;
    total integer;
    pass integer := 0;
    query text;
begin
    for _title.main_title, total in
        select main_title, count(main_title)
            from (
            select t.main_title, cr.name_id, cr.title_id
            from Crew_roles cr
            join Titles t on (cr.title_id = t.id)
            where t.main_title ilike '%'||partial_title||'%'
            union distinct
            select t.main_title, ar.name_id, ar.title_id
            from Actor_roles ar
            join Titles t on (ar.title_id = t.id)
            where t.main_title ilike '%'||partial_title||'%'
            union distinct
            select t.main_title, p.name_id, p.title_id
            from Principals p
            join Titles t on (p.title_id = t.id)
            where t.main_title ilike '%'||partial_title||'%'
           ) as a
        group by main_title, title_id
    loop
        pass := 1;
        query := _title.main_title||' has '||total||' cast and crew';
        return next query;
    end loop;
    
    if (pass = 0) then
        query := 'No matching titles';
        return next query;
    end if;
end;


$$ language plpgsql;






















