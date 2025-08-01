# from datetime import time, datetime
# import frappe
# import google.auth.transport.requests
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from frappe.utils.password import get_decrypted_password  # securely fetch password field

# def timedelta_to_time(td):
#     total_seconds = int(td.total_seconds())
#     hours = total_seconds // 3600
#     minutes = (total_seconds % 3600) // 60
#     seconds = total_seconds % 60
#     return time(hour=hours, minute=minutes, second=seconds)


# @frappe.whitelist()
# def generate_google_meet_link(docname):
#     try:
#         doc = frappe.get_doc("Interview", docname)

#         if doc.custom_google_meet_link:
#             return doc.custom_google_meet_link

#         user_email = doc.custom_applicant_email
#         summary = f"Interview with {user_email}"

#         from_time = timedelta_to_time(doc.from_time)
#         to_time = timedelta_to_time(doc.to_time)

#         start_time = datetime.combine(doc.scheduled_on, from_time).isoformat() + "+05:30"
#         end_time = datetime.combine(doc.scheduled_on, to_time).isoformat() + "+05:30"

#         # ✅ Load credentials from your custom DocType
#         oauth_doc = frappe.get_doc("Google meet oauth doc", {"app_name": "Googlemeetlinkdoc"})

#         client_id = oauth_doc.client_id
#         client_secret = get_decrypted_password("Google meet oauth doc", oauth_doc.name, "client_secret")
#         access_token = oauth_doc.access_token
#         refresh_token = oauth_doc.refresh_token

#         # 🛠️ Build credentials
#         creds = Credentials(
#             token=access_token,
#             refresh_token=refresh_token,
#             token_uri="https://oauth2.googleapis.com/token",
#             client_id=client_id,
#             client_secret=client_secret
#         )

#         # 🔄 Refresh token
#         creds.refresh(google.auth.transport.requests.Request())

#         # 🔁 Save updated token values
#         frappe.db.set_value("Google meet oauth doc", oauth_doc.name, {
#             "access_token": creds.token,
#             "refresh_token": creds.refresh_token or refresh_token
#         })

#         # 📅 Create the Google Meet event
#         service = build("calendar", "v3", credentials=creds)

#         event = {
#             "summary": summary,
#             "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
#             "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
#             "conferenceData": {
#                 "createRequest": {
#                     "requestId": frappe.generate_hash(),
#                     "conferenceSolutionKey": {"type": "hangoutsMeet"}
#                 }
#             },
#             "attendees": [{"email": user_email}]
#         }

#         created_event = service.events().insert(
#             calendarId='primary',
#             body=event,
#             conferenceDataVersion=1
#         ).execute()

#         meet_link = created_event["conferenceData"]["entryPoints"][0]["uri"]
#         doc.custom_google_meet_link = meet_link
#         doc.save()

#         return meet_link

#     except Exception as e:
#         frappe.log_error(title="Google Meet Link Error", message=frappe.get_traceback())
#         return f"Error creating Google Meet link: {e}"






# File: google_meet.py

from datetime import time, datetime

# Frappe framework imports
import frappe
from frappe.utils.password import get_decrypted_password  # for secure password access

# Google API imports
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def timedelta_to_time(td):
    """
    Convert a timedelta object (from_time, to_time fields) to a time object.
    This is necessary because Frappe stores time fields as timedelta.
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return time(hour=hours, minute=minutes, second=seconds)


@frappe.whitelist()
def generate_google_meet_link(docname):
    """
    Generates a Google Meet link for an Interview document using stored OAuth credentials.

    Args:
        docname (str): Name of the Interview document.

    Returns:
        str: Google Meet URL or an error message.
    """
    try:
        #  Get Interview document
        doc = frappe.get_doc("Interview", docname)

        # Return existing link if already generated
        if doc.custom_google_meet_link:
            return doc.custom_google_meet_link

        #  Prepare calendar event details
        user_email = doc.custom_applicant_email
        summary = f"Interview with {user_email}"

        from_time = timedelta_to_time(doc.from_time)
        to_time = timedelta_to_time(doc.to_time)

        start_time = datetime.combine(doc.scheduled_on, from_time).isoformat() + "+05:30"
        end_time = datetime.combine(doc.scheduled_on, to_time).isoformat() + "+05:30"

        #  Load credentials from your custom OAuth DocType
        oauth_doc = frappe.get_doc("Google meet oauth doc", {"app_name": "Googlemeetlinkdoc"})

        client_id = oauth_doc.client_id
        client_secret = get_decrypted_password("Google meet oauth doc", oauth_doc.name, "client_secret")
        access_token = oauth_doc.access_token
        refresh_token = oauth_doc.refresh_token

        #  Build Credentials object
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )

        # Refresh token if expired
        creds.refresh(google.auth.transport.requests.Request())

        #  Save new token values
        frappe.db.set_value("Google meet oauth doc", oauth_doc.name, {
            "access_token": creds.token,
            "refresh_token": creds.refresh_token or refresh_token  # Keep old refresh_token if new not returned
        })

        # Create Google Calendar event with Meet link
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Kolkata"
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": frappe.generate_hash(),
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    }
                }
            },
            "attendees": [
                {"email": user_email}
            ]
        }

        created_event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        #  Extract Meet link from created event
        meet_link = created_event["conferenceData"]["entryPoints"][0]["uri"]

        #  Save the Meet link back to the Interview document
        doc.custom_google_meet_link = meet_link
        doc.save()

        return meet_link

    except Exception as e:
        # Log error for debugging and return fallback error message
        frappe.log_error(title="Google Meet Link Error", message=frappe.get_traceback())
        return f"Error creating Google Meet link: {e}"
