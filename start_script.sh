source venv/bin/activate
if [[ $1 == "server" ]]
then
    python3 server.py
else
    python3 client.py
fi