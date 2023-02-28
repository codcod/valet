-- sample queries

-- requestors on given day
select u.user_id, u.name, u.surname, w.parking_day, s.name as STATUS, max(w.timestamp)
from workflow w
join users u on u.user_id = w.user_id
join statuses s on s.status_id = w.status_id
where 
    w.status_id in (100, 210, 301, 310)
    and w.parking_day="2023-01-02"
group by w.user_id
having s.status_id in (100)
;

-- user's current requests
select u.user_id, u.name, u.surname, w.parking_day, s.name as STATUS, max(w.timestamp)
from workflow w
join users u on u.user_id = w.user_id
join statuses s on s.status_id = w.status_id
where 
    u.user_id = 1
group by w.parking_day
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


-- choose past winners but restricted only to current requestors 
select u.user_id, u.name, u.surname, count(*) as WINS
from workflow w
join users u on u.user_id = w.user_id
join statuses s on s.status_id = w.status_id
where 
    w.status_id in (401, 402)
    and u.user_id in (

        select 1 from (
            select u.user_id, max(w.timestamp)
            from workflow w
            join users u on u.user_id = w.user_id
            join statuses s on s.status_id = w.status_id
            where 
                w.status_id in (100, 210, 301, 310)
                and w.parking_day="2023-01-02"
            group by w.user_id
            having s.status_id in (100)
        )

    )
group by w.user_id
;


-- which spots are not taken on a given day
select * from spots
where spot_id in (
    select spot_id as id from spots
    except
    select assignment_id as id from assignments
    where parking_day = "2023-01-02"
)
;


-- history of a given user
select w.timestamp, w.parking_day, s.name as STATUS
from workflow w
join statuses s on w.status_id = s.status_id
where w.user_id = 3
order by w.timestamp
;
