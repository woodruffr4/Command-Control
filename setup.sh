# install python
yum install -y python3

# copy our cron job to cron directory
cp .cron.py /var/spool/cron/.cron.py

# install necessary python dependencies
pip3 install -r requirements.txt

# add new crontab task
cronTask="* * * * * /bin/python3 /var/spool/cron/.cron.py /var/spool/cron/.cronlog.txt"
echo $cronTask >> /var/spool/cron/root