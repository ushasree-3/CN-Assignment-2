#!/bin/bash

# Extract the option value from "--option="
if [[ "$1" =~ ^--option=(.*)$ ]]; then
    option="${BASH_REMATCH[1]}"
else
    echo "Invalid usage. Correct format: ./run_script --option={a|b|c|d}"
    exit 1
fi

# Execute the corresponding script
case "$option" in
    a)
        echo "Running a.py"
        sudo python3 a.py
        ;;
    b)
        echo "Running b.py"
        sudo python3 b.py
        ;;
    c)
        echo "Running c.py"
        sudo python3 c.py
        ;;
    d)
        echo "Running d.py and loss=1..."
        sudo python3 d.py 1
        echo "Running d.py and loss=5..."
        sudo python3 d.py 5
        ;;
    *)
        echo "Invalid option. Usage: ./run_script --option={a|b|c|d}"
        exit 1
        ;;
esac
