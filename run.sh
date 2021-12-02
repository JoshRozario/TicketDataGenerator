#!/bin/bash
python3 ./Ticket\ Data\ Generator/test_dataGen.py
python3 ./Ticket\ Data\ Generator/dataGen.py -n 1000 -o data.json
python3 ./JSON\ to\ SQL/Converter.py
sqlite3 ./data.db < timeTill.sql
#sqlite3 ./data.db < select.sql
