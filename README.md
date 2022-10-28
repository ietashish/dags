# Splunk Alerts
Below are the details of Splunk alerts created on https://splunkes.or1.adobe.net/.
These alerts have been created manually from Splunk UI *(Setting -> Searches, reports, and alerts)*.

## Alert for drop in log volume
| Field                        | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Alert                        | GCP MAVLink alert: Drop in log volume                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Description                  | Raises an alert if any of the the sourcetypes that receive MAVLink GCP logs show a sudden drop in log volume.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Search                       | <pre>index=gcp sourcetype IN (gcp:asset, gcp:asset_feed, gcp:audit, gcp:command_center, gcp:command_center_feed)<br>\| stats count by sourcetype <br>\| append <br>    [\| makeresults count=5 <br>    \| streamstats count <br>    \| eval sourcetype=case(count==1, "gcp:asset", count==2, "gcp:asset_feed", count==3, "gcp:audit", count==4, "gcp:command_center", count==5, "gcp:command_center_feed") <br>    \| eval count=0 <br>    \| fields - _time, row] <br>\| stats sum(count) as count by sourcetype<br>\| search count < 10 </pre>|
| Time Range                   | Run on Cron Schedule -> Last 4 hours                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Cron Expression              | 0 */3 * * *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Expires                      | 7 days                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Trigger alert when           | Custom -> ```search count < 10```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Trigger                      | For each result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Throttle                     | False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Trigger Action               | Slack                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Slack trigger attributes** |
| Channel                      | #gcp-mavlink-alerts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Message                      | <pre>> *<$view_link$\|$name$>*<br>> *There seems to be a drop in volume of GCP MAVLink logs.*<br>> <br>> Splunk log sourcetype `$result.sourcetype$` received `$result.count$` events in last 4 hours which is unusually low.<br>> <br>> <$results_link$\|View results in Splunk></pre>                                                                                                                                                                                                                                                                                 |
| Attachments                  | None                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Fields                       | None                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Webhook URL                  | URL of form https://hooks.slack.com/services/xxxx/xxxx|

<br/>
<br/>

## Alert for checking deviation in Projects/Folders count
| Field                        | Value                                                                                                                                                            |
| ---------------------------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Alert                        | GCP MAVLink alert: Projects/Folders count                                                                                                                        |
| Description                  | Raises an alert if the number of distinct projects/folders/organizations found in gcp:asset sourcetype is lower than the last calculated count by more than 10%. |
| Search                       | <pre>index=gcp sourcetype=gcp:asset earliest=-4h <br>\| rename ancestors{} as ancestors_list <br>\| table ancestors_list <br>\| eval parent = mvindex(ancestors_list, 0) <br>\| stats dc(parent) as new_count <br>\| append <br>    [ search index=gcp sourcetype=gcp:asset earliest=-8h latest=-4h <br>    \| rename ancestors{} as ancestors_list <br>    \| table ancestors_list <br>    \| eval parent = mvindex(ancestors_list, 0) <br>    \| stats dc(parent) as old_count] <br>\| stats values(*) as * <br>\| eval diff_percent = (old_count-new_count)*100/old_count</pre> |
| Time Range                   | Run on Cron Schedule -> Last 15 minutes (Doesn't matter as "earliest" is being used in above search))                                                            |
| Cron Expression              | 30 */3 * * *                                                                                                                                                     |
| Expires                      | 7 days                                                                                                                                                           |
| Trigger alert when           | Custom -> ```search diff_percent>10```                                                                                                                           |
| Trigger                      | For each result                                                                                                                                                  |
| Throttle                     | False                                                                                                                                                            |
| Trigger Action               | Slack                                                                                                                                                            |
| **Slack trigger attributes** |
| Channel                      | #gcp-mavlink-alerts                                                                                                                                              |
| Message                      | <pre>> *<$view_link$\|$name$>*<br>> *There seems to be a drop in number of projects/folders in asset inventory logs of MAVLink GCP.*<br>> <br>> Found `$result.new_count$` projects/folders in `gcp:asset` sourcetype in last 4 hours which is lower than the last calculated count (`$result.old_count$`) by `$result.diff_percent$%`.<br>> <br>> <$results_link$\|View results in Splunk></pre>|
| Attachments                  | None                                                                                                                                                             |
| Fields                       | None                                                                                                                                                             |
| Webhook URL                  | URL of form https://hooks.slack.com/services/xxxx/xxxx                                                                                                           |