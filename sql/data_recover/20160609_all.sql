
--- 2016 2 リカバリ

delete pixiv_tag_daily from where  get_date = '2016-06-09 00:00:00';

select bases_id,"2016-06-09 00:00:00",search_word,total,"データ欠損 復旧対応",created_at, now() from pixiv_tag_hourly where get_date > '2016-06-09 00:00:00' and get_date < '2016-06-09 04:00:00' order by bases_id;

start transaction;

insert into pixiv_tag_daily (bases_id,get_date,search_word,total,note,created_at,updated_at)


select bases_id,"2016-06-09 00:00:00",search_word,total,"データ欠損 復旧対応",created_at, now() from pixiv_tag_hourly where get_date > '2016-06-09 00:00:00' and get_date < '2016-06-09 04:00:00';

commit;


--- 2016 1 リカバリ

select bases_id,"2016-06-09 00:00:00",search_word,total,"データ欠損 復旧対応",created_at, now() from pixiv_tag_hourly where get_date > '2016-06-09 00:00:00' and get_date < '2016-06-09 05:00:00' and bases_id < 321 order by bases_id;

start transaction;

insert into pixiv_tag_daily (bases_id,get_date,search_word,total,note,created_at,updated_at)


select bases_id,"2016-06-09 00:00:00",search_word,total,"データ欠損 復旧対応",created_at, now() from pixiv_tag_hourly where get_date > '2016-06-09 00:00:00' and get_date < '2016-06-09 05:00:00' and bases_id < 321;

commit;