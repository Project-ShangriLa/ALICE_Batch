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
every 2.hour do
  command "source .bashrc;cd $ALICE_BATCH;python3 alice.py;cd $ALICE_WEB;bundle exe ruby gen_pixiv_ranking.rb -o /usr/share/nginx/html/pix/index.html"
end

every :day, :at => '00:35am' do
  command "source .bashrc;cd $ALICE_BATCH;python3 alice.py -d"
end

