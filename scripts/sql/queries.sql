-- sample queries

-- requestors on given day
select u.user_id, u.name, u.surname, w.parking_day, s.name as STATUS, max(w.timestamp)
from workflow w
join users u on u.user_id = w.user_id
join statuses s on s.status_id = w.status_id
where 
    w.status_id in (100, 210)
    and w.parking_day="2023-01-01"
group by w.user_id
having s.status_id in (100)
;


-- how many wins so far each user has
select u.user_id, u.name, u.surname, count(*) as WINS
from workflow w
join users u on u.user_id = w.user_id
join statuses s on s.status_id = w.status_id
where 
    w.status_id in (401, 402)
group by w.user_id
;


-- add new winner
/*insert into workflow (timestamp, parking_day, user_id, status_id)
values (now(), "2023-01-01", 3, 301)
;*/


-- which spots are not taken on a given day
select * from spots
where spot_id in (
    select spot_id as id from spots
    except
    select assignment_id as id from assignments
    where parking_day = "2023-01-01"
)
;


-- history of a given user
select w.timestamp, w.parking_day, s.name as STATUS
from workflow w
join statuses s on w.status_id = s.status_id
where w.user_id = 1
order by w.timestamp
;
