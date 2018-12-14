wmic bios get serialnumber > serial.txt
python3 main.py
REM del "serial.txt"
