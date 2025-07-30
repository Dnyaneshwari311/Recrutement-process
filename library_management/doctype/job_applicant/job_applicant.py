# import frappe
# from frappe import _

# @frappe.whitelist()
# def send_shortlist_email(docname):
#     doc = frappe.get_doc("Job Applicant", docname)

#     if not doc.email_id:
#         frappe.throw(_("No email address found for the applicant."))

#     message = f"""
#     <p>Dear {doc.applicant_name},</p>

#     <p>Congratulations! You have been <strong>shortlisted</strong> for the position of <strong>{doc.job_title}</strong> at Excellent Minds Software Technologies.</p>

#     <p>Our team will reach out to you shortly with the interview schedule.</p>

#     <p>Best regards,<br>
#     HR Department<br>
#     Excellent Minds Software Technologies Pvt. Ltd.</p>
#     """

#     try:
#         frappe.sendmail(
#             recipients=[doc.email_id],
#             subject="Shortlisted for Interview – Excellent Minds",
#             message=message,
#             reference_doctype=doc.doctype,
#             reference_name=doc.name,
#         )
#     except Exception:
#         frappe.log_error(frappe.get_traceback(), "Shortlisting Email Failed")
#         frappe.throw(_("Failed to send the email. Please check email configuration."))

#     frappe.msgprint(_("Shortlist email sent successfully."))



# Import Frappe framework and translation utility
import frappe
from frappe import _  # Used for translatable strings

# Allow this function to be called via client-side (JS) or API (whitelisted)
@frappe.whitelist()
def send_shortlist_email(docname):
    """
    Sends a shortlist email to the applicant based on the provided Job Applicant document name.
    """

    # Fetch the Job Applicant document using the provided name
    doc = frappe.get_doc("Job Applicant", docname)

    # Check if the applicant has an email address
    if not doc.email_id:
        # Throw a validation error if email is missing
        frappe.throw(_("No email address found for the applicant."))

    # Compose the email message using HTML formatting and f-string to personalize
    message = f"""
    <p>Dear {doc.applicant_name},</p>

    <p>Congratulations! You have been <strong>shortlisted</strong> for the position of 
    <strong>{doc.job_title}</strong> at Excellent Minds Software Technologies.</p>

    <p>Our team will reach out to you shortly with the interview schedule.</p>

    <p>Best regards,<br>
    HR Department<br>
    Excellent Minds Software Technologies Pvt. Ltd.</p>
    """

    try:
        # Send the email using Frappe's built-in email function
        frappe.sendmail(
            recipients=[doc.email_id],         # Recipient is the applicant
            subject="Shortlisted for Interview – Excellent Minds",  # Email subject
            message=message,                   # Email body
            reference_doctype=doc.doctype,     # Link to the Job Applicant DocType
            reference_name=doc.name            # Link to the specific applicant record
        )

    except Exception:
        # Log the error with traceback in case email sending fails
        frappe.log_error(frappe.get_traceback(), "Shortlisting Email Failed")

        # Notify the user with a user-friendly error message
        frappe.throw(_("Failed to send the email. Please check email configuration."))

    # Show a success message in the UI if the email was sent successfully
    frappe.msgprint(_("Shortlist email sent successfully."))
