# RuView SMART FINAL v1.0.0
Professional Build - English Only

## Features
- Smart Learning 30 sec - Learns YOUR home baseline
- Normal vs Abnormal Limits - Adaptive, not fixed
- Zone ID - Near Router / Living Room / Far
- Night Guard 00:00-05:00
- Elderly Care - Alert if no movement 30 min
- Fall Detection - Sudden RSSI drop >20
- SOS Button - Loud notification
- Event Log - Last 100 events in events.json
- Privacy - Local only, No data to other phone, Visible notification, Requires START press

## Install
Share APK to family phone -> Install -> Allow Location + Notification -> Open App -> Press START -> Stay still 30 sec to learn -> Done

## Restore Point
If anything breaks: bash restore.sh ~/RuView-Backup/<your-backup>.tar.gz

## Note
This app uses WiFi RSSI only. It does NOT identify WHO is walking, only WHERE (zone) and HOW STRONG movement is. Real body skeleton needs ESP32 + Laptop, separate advanced project.
