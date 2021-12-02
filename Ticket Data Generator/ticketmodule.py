import json
import datetime


# lists of possible activty attributes
address = ['231 Test street', '520 Warwick Road',
           "452 Denzel Lane", "12 The Boulevard"]
categories = ['Phone', 'Computer', 'Printer', 'Monitor',
              'Keyboard', 'Mouse', 'Speaker', 'Headphone', 'Cable', 'Other']
contacted_customers = [True, False]
issue_types = ['Incident', 'Question', 'Problem', 'Task', 'Other']
status = ['Open', 'Pending', 'Resolved', 'Closed']
groups = ['refund', 'exchange', 'replacement', 'other']
products = ['mobile', 'desktop', 'other']


class ActivityList:
    def __init__(self, metadata):
        self.metadata = metadata
        self.activities_data = []

    def activity_count(self):
        return len(self.activities_data)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Metadata:
    def __init__(self, start_at, end_at, activity_count):
        self.start_at = start_at
        self.end_at = end_at
        self.activity_count = activity_count


class ActivityData:
    def __init__(self, perfomed_at, ticket_id, performer_type, performer_id, activity):
        self.performed_at = perfomed_at
        self.ticket_id = ticket_id
        self.performer_type = performer_type
        self.performer_id = performer_id
        self.activity = activity


class Activity:
    def __init__(self):
        pass


class ActivityNote(Activity):
    def __init__(self, note):
        self.note = note


class ActivityOrder(Activity):
    def __init__(self, shipping_address, shipment_date, category, contacted_customer, issue_type, source, status, priority, group, agent_id, requester, product):
        self.shipping_address = shipping_address
        self.shipment_date = shipment_date
        self.category = category
        self.contacted_customer = contacted_customer
        self.issue_type = issue_type
        self.source = source
        self.status = status
        self.priority = priority
        self.group = group
        self.agent_id = agent_id
        self.requester = requester
        self.product = product


class Note:
    def __init__(self, id, type):
        self.id = id
        self.type = type
