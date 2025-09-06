if [[ $(python3 --version 2> /dev/null) ]]
then
    python3 -m venv venv
    source venv/bin/activate
    pip install prompt_toolkit
    deactivate
elif [[ $(python --version 2> /dev/null) ]]
then
    python -m venv venv
    source venv/bin/activate
    pip install prompt_toolkit
    deactivate
else
    echo "Please install python first"
fi