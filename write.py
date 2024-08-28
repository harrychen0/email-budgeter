def write_to_google_sheets(service, spreadsheet_id, range, data):
    # Prepare the data for writing
    if data:
        values = [[i for i in data[0]]]  # Headers
        for msg in data:
            details = [i for i in msg.values()]
            values.append(details)
        body = {
            'values': values
        }

        # Call the Sheets API to update the spreadsheet
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Successfully written to file")