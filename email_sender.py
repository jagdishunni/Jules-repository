import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from google.cloud import secretmanager

class EmailSender:
    def __init__(self, project_id=None):
        self.api_key = self.get_sendgrid_key(project_id)
        if self.api_key:
            self.sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
        else:
            print("Warning: No SendGrid API key found. Using mock sender.")
            self.sg = None

    def get_sendgrid_key(self, project_id):
        """Retrieves SendGrid key from Secret Manager or environment."""
        # Check env var first
        key = os.environ.get("SENDGRID_API_KEY")
        if key:
            return key

        # Fallback to Secret Manager if project_id is provided
        if project_id:
            try:
                client = secretmanager.SecretManagerServiceClient()
                secret_name = f"projects/{project_id}/secrets/SENDGRID_API_KEY/versions/latest"
                response = client.access_secret_version(request={"name": secret_name})
                return response.payload.data.decode("UTF-8")
            except Exception as e:
                print(f"Warning: Could not access secret manager: {e}")
                return None
        return None

    def send_email(self, html_content, recipient):
        """Sends an email with the newsletter content."""
        if not self.sg:
            print(f"Mock email sent to {recipient}")
            return True

        message = Mail(
            from_email='newsletter@example.com',
            to_emails=recipient,
            subject='Daily AI Intelligence Report',
            html_content=html_content
        )
        try:
            response = self.sg.send(message)
            print(f"Email sent successfully. Status Code: {response.status_code}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

if __name__ == "__main__":
    sender = EmailSender()
    sender.send_email("<h1>Hello World</h1>", "test@example.com")
