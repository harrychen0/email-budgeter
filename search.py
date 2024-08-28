import re
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode
from collections import deque
def extract_purchase_details(body, regex, msg_id):
    # Search the body with the defined pattern
    match = re.search(re.compile(regex), body)

    if match:
        # Extract the details using the named groups (remove whitespace with .strip())
        purchase_details = {
            'msg_id' : msg_id,
            'date': match.group('date'),
            'amount': match.group('amount'),
            'store': match.group('store').strip(),
            'location': match.group('location').strip()
        }
        return purchase_details
    return None

def search_messages(service, query, regex):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    message_details = deque()

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        # Extract the body from the message
        if 'parts' in msg_data['payload']:
            for part in msg_data['payload']['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    body = urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        else:
            body = urlsafe_b64decode(msg_data['payload']['body']['data']).decode('utf-8')

        # Store the extracted details
        body_details = extract_purchase_details(body, regex, msg_id)
        if body_details:
            print(body_details)
        else:
            print("Could not extract purchase details. ", body[:50])
        message_details.appendleft(body_details)

    return message_details