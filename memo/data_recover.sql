
start transaction

insert into pixiv_tag_daily (bases_id,get_date,search_word,total,note,created_at,updated_at)

select bases_id,"2016-03-28 00:00:00",search_word,total,"データ欠損 復旧対応",created_at, now() from pixiv_tag_hourly where get_date > '2016-03-28 00:00:00' and get_date < '2016-03-28 01:00:00' and bases_id > 294 limit 24;

commit;


start transaction

insert into pixiv_tag_daily (bases_id,get_date,search_word,total,note,created_at,updated_at)

select bases_id,"2016-03-28 00:00:00",search_word,total,"データ欠損 復旧対応",created_at, now() from pixiv_tag_hourly where get_date > '2016-03-28 00:00:00' and get_date < '2016-03-28 01:00:00' and bases_id > 318 limit 2;

commit;