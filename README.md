# Linux server security monitoring

## Goal

Monitoring of security events on a Linux server. Providing push notifications of all shell logins and unknown IPs connections. Logging all failed login attempts.

## How to use

1. Install the required python packages:
```bash
pip install -r requirements.txt
```

2. Create and fill custom `config.json` file:
```bash
cp config.mock.json config.json
# edit the file
# Need to get the pushbullet token - https://docs.pushbullet.com/
```

3. Generate and deploy the services:
```bash
make deploy # ./deploy_services.sh
```

4. Check all is fine:
```bash
make status # ./status.sh
```

## Individual services

### Shell login monitoring

`login_monitor.py` - using `last` cmd to look at the last shell logins and send a push notification.

### Auth monitoring

`auth_monitor.py` - reading `/var/log/auth.log`, sending notifications about all logins from unknown IPs and logging all the failed login attempts.

## Results

Monitoring is set up as a service, and therefore runs all the time, even after reboot.
