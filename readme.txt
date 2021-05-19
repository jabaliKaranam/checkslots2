Script will query CoWin servers to check for slots in a specific center for 5 days from current day.
You can run it manually or automate it or deploy to a server and keep it running on a schedule.
Note that we are limited to 100 requests every 5 minutes.
Several hosts like AWS have been blocked.

Set the values in properties.txt using the below.
Get CENTER_ID from https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=DISTRICT_ID&date=DATE
Get DISTRICT_ID from https://cdn-api.co-vin.in/api/v2/admin/location/districts/STATE_ID
Get STATE_ID from https://cdn-api.co-vin.in/api/v2/admin/location/states
MODE relates to if you want to use the IFTTT integration with webhooks. If you are familiar with IFTTT you can set that up too. If you wish to use IFTTT MODE should be 1. Else 0.
You can setit  to any other value and add something like a mail component.

