cd /Users/upakalapati/Downloads

nohup sh /Users/upakalapati/Downloads/kibana-7.0.0-darwin-x86_64/bin/kibana > /Users/upakalapati/Downloads/kibana_log.out 2>&1 &

nohup sh /Users/upakalapati/Downloads/elasticsearch-7.0.0/bin/elasticsearch  > /Users/upakalapati/Downloads/elk_log.out 2>&1 &

nohup sh /Users/upakalapati/Downloads/logstash-7.0.0/bin/logstash -f /Users/upakalapati/Downloads/logstash-7.0.0/config/logstash.conf > /Users/upakalapati/Downloads/log_stash_log.out 2>&1 &


while :; do
  sleep 360
  nohup sh /Users/upakalapati/Downloads/logstash-7.0.0/bin/logstash -f /Users/upakalapati/Downloads/logstash-7.0.0/config/logstash.conf > /Users/upakalapati/Downloads/log_stash_log.out 2>&1 &
  sleep 360
done