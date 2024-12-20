# TCP Chat App
## Fall 2024 EECS 563 Extra Credit Project

## Authors
- William Morris [morriswa]


## Setup guide

- This application depends on:
  - python@3.12
  - python-tk@3.12
  - postgresql


- After installing dependencies, enter postgres console (psql)
logged in as database admin user and enter the following statements...

      CREATE ROLE tcp_chat_app_role with login password 'password';
      CREATE DATABASE tcp_chat_app;
      GRANT CREATE ON DATABASE tcp_chat_app TO tcp_chat_app_role;
      \c tcp_chat_app;
      GRANT CREATE ON SCHEMA public TO tcp_chat_app_role;
- Open project root directory in terminal
- Install Project environment

      python3.12 -m venv .
- Activate Project environment
    - Mac/Linux

          source bin/activate
        - NOTE: to deactivate project environment

              deactivate
        - NOTE: to reset project environment 

              rm -rf bin include lib pyvenv.cfg
    - Windows Powershell

          .\Scripts\activate
        - NOTE: to deactivate project environment

              .\Scripts\deactivate.bat
        - NOTE: to reset project environment 

              rm -r include
              rm -r lib 
              rm -r scripts
              rm -r pyvenv.cfg
- Install python dependencies with PIP 

      pip install -r requirements.txt
- Ensure postgresql server is running
- Client and Server scripts must be run in virtual environment for the app 
to function properly
- Server can be started using

      python ./server/main.py
- Client can be executed using

      python ./client/main.py
