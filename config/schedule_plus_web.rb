# Use this file to easily define all of your cron jobs.
#
# It's helpful, but not entirely necessary to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron

# Example:
#
# set :output, "/path/to/my/cron_log.log"
#
# every 2.hours do
#   command "/usr/bin/some_great_command"
#   runner "MyModel.some_method"
#   rake "some:great:rake:task"
# end
#
# every 4.days do
#   runner "AnotherModel.prune_old_records"
# end

# Learn more: http://github.com/javan/whenever
set :output, "/var/log/cron.log"
every 4.hour do
  command "source .bashrc;cd $ALICE_BATCH;python3 alice.py -y 2016 -c 1;cd $ALICE_WEB;bundle exe ruby gen_pixiv_ranking.rb -y 2016 -c 1 -o /usr/share/nginx/html/pix/index.html"
end

every :day, :at => '00:35am' do
  command "source .bashrc;cd $ALICE_BATCH;python3 alice.py -y 2016 -c 1 -d"
end

every 3.hour do
  command "source .bashrc;cd $ALICE_BATCH;python3 alice.py -y 2016 -c 2;cd $ALICE_WEB;bundle exe ruby gen_pixiv_ranking.rb -y 2016 -c 2 -o /usr/share/nginx/html/pix/ranking2016spring.html"
end

#bundle exe ruby gen_pixiv_ranking.rb -o ranking2016spring.html -y 2016 -c 1
every :day, :at => '00:40am' do
  command "source .bashrc;cd $ALICE_BATCH;python3 alice.py  -y 2016 -c 2 -d"
end

