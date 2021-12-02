import unittest
import dataGen
from datetime import datetime as dt


class TestDataGen(unittest.TestCase):

    # Test that creating dates works
    def test_createDate(self):
        date = dataGen.createDate()
        start_date = dt.strptime(date[0], "%d-%m-%Y %H:%M:%S +0000")
        end_date = dt.strptime(date[1], "%d-%m-%Y %H:%M:%S +0000")
        self.assertTrue(start_date < end_date)

    # Test that creating tickets works
    def test_createTickets(self):
        tickets = dataGen.createTickets(1)
        self.assertEqual(tickets.metadata.activity_count, 4)
        self.assertEqual(len(tickets.activities_data), 4)

    # Test that creating tickets with multiple tickets works
    def test_createTickets_multiple(self):
        tickets = dataGen.createTickets(5)
        self.assertEqual(tickets.metadata.activity_count, 20)
        self.assertEqual(len(tickets.activities_data), 20)

    # Test that tickets have consistent attributes
    def test_each_ticket_activites_have_same_attributes(self):
        tickets = dataGen.createTickets(1)
        for i in range(len(tickets.activities_data)-1):
            self.assertEqual(
                tickets.activities_data[i].ticket_id, tickets.activities_data[i+1].ticket_id)
            self.assertEqual(
                tickets.activities_data[i].performer_id, tickets.activities_data[i+1].performer_id)
            self.assertEqual(
                tickets.activities_data[i].activity.shipping_address, tickets.activities_data[i+1].activity.shipping_address)
            self.assertEqual(
                tickets.activities_data[i].activity.category, tickets.activities_data[i+1].activity.category)
            self.assertEqual(
                tickets.activities_data[i].activity.agent_id, tickets.activities_data[i+1].activity.agent_id)

    # Test that each ticket has a unique ticket_id
    def test_each_ticket_has_unique_id(self):
        tickets = dataGen.createTickets(1)
        ticket_ids = []
        for i in range(len(tickets.activities_data)):
            if tickets.activities_data[i].activity.status == "Open":
                ticket_ids.append(tickets.activities_data[i].ticket_id)
        self.assertEqual(len(ticket_ids), len(set(ticket_ids)))


if __name__ == '__main__':
    print("Running tests...")
    unittest.main()
