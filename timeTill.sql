UPDATE ticket_times
SET	time_spent_open = SUBSTR(SUBSTR("0000000"||time_spent_open,LENGTH(time_spent_open),8),1,2)*3600 +
	SUBSTR(SUBSTR("0000000"||time_spent_open,LENGTH(time_spent_open),8),4,2)*60 +
	SUBSTR(SUBSTR("0000000"||time_spent_open,LENGTH(time_spent_open),8),7,2),
	time_spent_waiting_on_customer = SUBSTR(SUBSTR("0000000"||time_spent_waiting_on_customer,LENGTH(time_spent_waiting_on_customer),8),1,2)*3600 +
    SUBSTR(SUBSTR("0000000"||time_spent_waiting_on_customer,LENGTH(time_spent_waiting_on_customer),8),4,2)*60 +
    SUBSTR(SUBSTR("0000000"||time_spent_waiting_on_customer,LENGTH(time_spent_waiting_on_customer),8),7,2),
    time_spent_waiting_for_response = SUBSTR(SUBSTR("0000000"||time_spent_waiting_for_response,LENGTH(time_spent_waiting_for_response),8),1,2)*3600 +
    SUBSTR(SUBSTR("0000000"||time_spent_waiting_for_response,LENGTH(time_spent_waiting_for_response),8),4,2)*60 +
    SUBSTR(SUBSTR("0000000"||time_spent_waiting_for_response,LENGTH(time_spent_waiting_for_response),8),7,2),
    time_till_resolution = SUBSTR(SUBSTR("0000000"||time_till_resolution,LENGTH(time_till_resolution),8),1,2)*3600 +
    SUBSTR(SUBSTR("0000000"||time_till_resolution,LENGTH(time_till_resolution),8),4,2)*60 +
    SUBSTR(SUBSTR("0000000"||time_till_resolution,LENGTH(time_till_resolution),8),7,2),
    time_to_first_response = SUBSTR(SUBSTR("0000000"||time_to_first_response,LENGTH(time_to_first_response),8),1,2)*3600 +
    SUBSTR(SUBSTR("0000000"||time_to_first_response,LENGTH(time_to_first_response),8),4,2)*60 +
    SUBSTR(SUBSTR("0000000"||time_to_first_response,LENGTH(time_to_first_response),8),7,2)