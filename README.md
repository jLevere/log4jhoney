# log4jhoney


Dead simple log4j honeypot based on a flask webserver.

Uses regex to identify posible exploit attempts and post the jsonifyed request in question to a discord webhook.

Move the service file to /etc/systemd if you want to run it with systemd.  Also, add a discord webhook to the discord_webhook variable in log4jhoney.py