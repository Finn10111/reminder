# reminder
A simple python Flask application which adds reminders to every event in a given ICS file.

See it in action at https://reminder.pimux.de

## Installation

### Docker

`docker run code.f2n.me/finn/reminder:latest`

### non-Docker

Clone the repo, install Python virtual environment, configure webserver (or use some wsgi server)

```
git clone https://code.f2n.me/finn/reminder.git reminder
cd reminder
virtualenv .
. bin/activate
pip install -r requirements.txt
cp apache_sample_config.php /etc/apache2/sites-available/my-reminder.exmaple.org.conf
a2ensite my-reminder.exmaple.org.conf
```
