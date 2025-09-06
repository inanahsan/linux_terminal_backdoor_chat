source venv/bin/activate
if [[ $(python3 --version 2> /dev/null) ]]
then
    if [[ $1 == "server" ]]
    then
        python3 server.py
    else
        python3 client.py
    fi
elif [[ $(python --version 2> /dev/null) ]]
then
    if [[ $1 == "server" ]]
    then
        python server.py
    else
        python client.py
    fi
fi
deactivate