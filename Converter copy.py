import json
import sqlite3
from datetime import datetime as dt

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Delete previous data
cursor.execute('DROP TABLE IF EXISTS ticket_ids')
cursor.execute('DROP TABLE IF EXISTS ticket_changes')
cursor.execute('DROP TABLE IF EXISTS activity_orders')
cursor.execute('DROP TABLE IF EXISTS activity_notes')
cursor.execute('DROP TABLE IF EXISTS ticket_times')

# Create tables
cursor.execute("""CREATE TABLE ticket_ids(
    ticket_id INTEGER PRIMARY KEY
    )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS ticket_changes(
    ticket_id INTEGER,
    performed_at DATETIME,
    performer_type TEXT,
    performer_id INTEGER,
    FOREIGN KEY(ticket_id) REFERENCES ticket_ids(ticket_id)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS activity_orders(
    ticket_id INTEGER,
    shipping_address TEXT,
    shipment_date TEXT,
    category TEXT,
    contacted_customer TEXT,
    issue_type TEXT,
    source INTEGER,
    status TEXT,
    priority INTEGER,
    group_name TEXT,
    agent_id INTEGER,
    reques INTEGER,
    product TEXT,
    FOREIGN KEY(ticket_id) REFERENCES ticket_ids(ticket_id)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS activity_notes(
    ticket_id INTEGER,
    note_id INTEGER,
    note_type INTEGER,
    FOREIGN KEY(ticket_id) REFERENCES ticket_ids(ticket_id)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS ticket_times(
    ticket_id INTEGER,
    time_spent_open TIME,
    time_spent_waiting_on_customer TIME,
    time_spent_waiting_for_response TIME,
    time_till_resolution TIME,
    time_to_first_response TIME,
    FOREIGN KEY(ticket_id) REFERENCES ticket_ids(ticket_id)
    )""")


# convert dates to correct form
def convert_date(date):
    date = date.split('+')[0]
    date = date.split('-')
    date2 = date[2].strip().split()
    date = date2[0] + '-' + date[1] + '-' + date[0] + ' ' + date2[1]
    return date


# function to calculate time spent
def calc_time_spent(open_time, close_time):
    open_time = dt.strptime(open_time, '%d-%m-%Y %H:%M:%S +0000')
    close_time = dt.strptime(close_time, '%d-%m-%Y %H:%M:%S +0000')
    time_spent = (close_time - open_time)
    # print(time_spent)
    return str(time_spent)


# load json file and set up variables
json_file = json.load(open('data.json'))
activity_count = json_file['metadata']['activity_count']
count = 0
ticket_id = 0

# load data into database

for i in range(0, activity_count):
    print("--- Loading data into database ---")
    prev_ticket_id = ticket_id

    performed_at = json_file['activities_data'][i]['performed_at']
    performed_at2 = convert_date(performed_at)
    ticket_id = json_file['activities_data'][i]['ticket_id']
    perfomer_type = json_file['activities_data'][i]['performer_type']
    performer_id = json_file['activities_data'][i]['performer_id']

    cursor.execute("""INSERT INTO ticket_changes VALUES(?, ?, ?, ?)""",
                   (ticket_id, performed_at2, perfomer_type, performer_id))

    activity = json_file['activities_data'][i]['activity']

    if("note" in activity):
        note_id = activity['note']['id']
        note_type = activity['note']['type']
        cursor.execute("""INSERT INTO activity_notes VALUES(?, ?, ?)""",
                       (ticket_id, note_id, note_type))
    else:
        shipping_address = activity['shipping_address']
        shipment_date = activity['shipment_date']
        category = activity['category']
        contacted_customer = activity['contacted_customer']
        issue_type = activity['issue_type']
        source = activity['source']
        status = activity['status']
        priority = activity['priority']
        group_name = activity['group']
        agent_id = activity['agent_id']
        requester = activity['requester']
        product = activity['product']

        cursor.execute("""INSERT INTO activity_orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (ticket_id, shipping_address, shipment_date, category, contacted_customer, issue_type, source, status, priority, group_name, agent_id, requester, product))

    if count == 0:
        cursor.execute("""INSERT INTO ticket_ids VALUES(?)""",
                       (ticket_id,))
        open_time = performed_at
        prev_contact = False

        if prev_ticket_id != 0:
            print(prev_ticket_id, ticket_id)
            cursor.execute("""INSERT INTO ticket_times VALUES(?, ?, ?, ?, ?,?)""",
                           (prev_ticket_id, time_open, time_waiting_on_customer_, time_waiting_for_response, time_till_resolution, time_to_response))

    count += 1

    if count == 2:
        #print("time spent open")
        time_open = calc_time_spent(open_time, performed_at)

    if contacted_customer == True:
        #print("time spent waiting on customer")
        prev_contact = True
        time_waiting_on_customer_ = calc_time_spent(open_time, performed_at)

    if status == 'Resolved':
        #print("time spent waiting for response")
        time_waiting_for_response = calc_time_spent(open_time, performed_at)

    if status == 'Closed':
        #print("time till resolution")
        time_till_resolution = calc_time_spent(open_time, performed_at)
        count = 0

    if status == 'Pending':
        #print("time to first response")
        time_to_response = calc_time_spent(open_time, performed_at)

connection.commit()
print("Data inserted successfully")
