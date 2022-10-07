# install python
yum install -y python3

# copy our cron job to cron directory and create log file
cp .cron.py /var/spool/cron/.cron.py
touch /var/spool/cron/.cronlog.txt

# install necessary cron job python dependencies
pip3 install -r requirements.txt

# add new crontab task
cronTask="* * * * * /bin/python3 /var/spool/cron/.cron.py $1 >> /var/spool/cron/.cronlog.txt 2>&1"
echo "$cronTask" >> /var/spool/cron/root