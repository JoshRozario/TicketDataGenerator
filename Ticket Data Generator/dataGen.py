# import required packages
import argparse
import sys
import random
from datetime import date, timedelta, datetime as dt

from ticketmodule import *


# function to create realistic date
def createDate():
    start_day = random.randint(1, 28)
    start_month = random.randint(1, 12)

    end_day = random.randint(start_day, 28)
    end_month = random.randint(start_month, 12)

    start_at = dt(2021, start_month, start_day) + \
        0.1 * timedelta(days=1)
    end_at = dt(2021, end_month, end_day) + \
        0.35 * timedelta(days=1)

    start_at = start_at.strftime("%d-%m-%Y %H:%M:%S +0000")
    end_at = end_at.strftime("%d-%m-%Y %H:%M:%S +0000")

    return start_at, end_at


# function to create ActivityNote
def createActivityNote(ticket_id, start_time, performer_type, performer_id):
    note_id = random.randint(100000, 999999)
    note_type = random.randint(1, 5)
    return ActivityData(start_time, ticket_id, performer_type, performer_id, ActivityNote(Note(note_id, note_type)))


# function to create ActivityOrder
def createActivityOrder(ticket_id, status_step, date, shipment_date, agent_id, shipping_address, category, contacted_customer, issue_type, source, group, product):

    return ActivityData(perfomed_at=date, ticket_id=ticket_id,
                        performer_type="agent", performer_id=agent_id,
                        activity=ActivityOrder(shipping_address, shipment_date, category,
                                               contacted_customer, issue_type,
                                               source, status[status_step], random.randint(
                                                   1, 5), group, agent_id,
                                               random.randint(100000, 999999),  product))


# wrapper function to create activity order or activity note
def createActivity(step, ticket_id, date, unique_id, shipping_address, category, contacted_customer, issue_type, source, group, product):
    shipment_date = date.strftime("%d %b, %Y")
    date = date.strftime("%d-%m-%Y %H:%M:%S +0000")
    if random.random() < 0.0:
        return createActivityNote(ticket_id, date, "user", unique_id)
    else:
        return createActivityOrder(ticket_id, step, date, shipment_date, unique_id, shipping_address, category, contacted_customer, issue_type, source, group, product)


# function to create n number of tickets with 4n activities
def createTickets(n_tickets):
    date = createDate()
    start_date = dt.strptime(date[0], "%d-%m-%Y %H:%M:%S +0000")
    end_date = date[1]
    metadata = Metadata(start_at=start_date.strftime("%d-%m-%Y %H:%M:%S +0000"), end_at=end_date,
                        activity_count=0)
    activityList = ActivityList(metadata)
    count = 0
    ticket_id = 100

    # randomize and insert consistent atrributes into the relavent ticket
    for i in range(n_tickets):
        ticket_id += 1
        shipping_address = random.choice(address)
        issue_type = random.choice(issue_types)
        category = random.choice(categories)
        contacted_customer = False
        product = random.choice(products)
        source = random.randint(1, 5)
        group = random.choice(groups)

        start_date = start_date + timedelta(minutes=random.randint(5, 20))
        step = 0
        unique_id = random.randint(100000, 999999)

        while step != 4:
            if contacted_customer != True and step != 0:
                contacted_customer = random.choice(contacted_customers)
            if step == 3:
                contacted_customer = True
            activityList.activities_data.append(
                createActivity(step, ticket_id, start_date, unique_id, shipping_address, category, contacted_customer, issue_type, source, group, product))
            start_date = start_date + timedelta(minutes=random.randint(1, 10))
            step += 1
            count += 1
        end_date = start_date + timedelta(days=1)

    activityList.metadata.activity_count = count
    activityList.metadata.end_at = end_date.strftime("%d-%m-%Y 09:59:59 +0000")
    return activityList


# main function
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Takes arguments for number of tickets to be generated')
    parser.add_argument('-n', '--number', type=int,
                        help='Number of tickets to be generated')
    parser.add_argument('-o', '--output', type=str, help='Output file name')

    if len(sys.argv) > 3:
        tickets = createTickets(parser.parse_args().number).toJSON()
        with open(parser.parse_args().output, 'w') as f:
            f.write(tickets)
        print("File saved as: ", parser.parse_args().output)
        sys.exit(1)
    else:
        print("arguments not provided, format: -n <number of tickets> -o <output file>")
        sys.exit(1)
