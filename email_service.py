import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service for sending emails via SMTP.
    Supports template rendering and error handling.
    """

    def __init__(self):
        """
        Initialize EmailService with SMTP configuration from environment.
        
        Environment variables:
        - SMTP_HOST: SMTP server hostname (default: smtp.gmail.com)
        - SMTP_PORT: SMTP server port (default: 587)
        - SENDER_EMAIL: Email address to send from
        - SENDER_PASSWORD: SMTP password/app token
        """
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        
        # Initialize Jinja2 template environment
        template_dir = os.path.join(os.path.dirname(__file__), "templates", "emails")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )

    def _validate_config(self) -> bool:
        """
        Validate that all required SMTP configuration is present.
        
        Returns:
            bool: True if config is valid, False otherwise
        """
        # TODO: Implement configuration validation
        # Check that sender_email and sender_password are set
        # Return False if any required config is missing
        # Log warning if config is incomplete
        return True

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render an email template with the given context.
        
        Args:
            template_name: Name of the template file (e.g., 'user_joined_group.html')
            context: Dictionary of variables to pass to the template
            
        Returns:
            str: Rendered HTML content
            
        Raises:
            TemplateNotFound: If the template file does not exist
        """
        # TODO: Implement template rendering
        # Load template using self.jinja_env.get_template()
        # Render with context dict
        # Return rendered string
        # Handle TemplateNotFound and log appropriately
        pass

    def send_email(
        self,
        recipient: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> bool:
        """
        Send an email via SMTP.
        
        Args:
            recipient: Email address of recipient
            subject: Email subject line
            html_body: HTML content of email
            text_body: Plain text fallback content (optional)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # TODO: Implement synchronous SMTP sending
        # Validate recipient email format
        # Create MIMEMultipart message
        # Attach text_body as alternative if provided
        # Attach html_body
        # Connect to SMTP server with TLS
        # Send message
        # Log success/failure
        # Return success boolean
        # Handle exceptions: SMTPAuthenticationError, SMTPException, etc.
        pass

    def send_email_with_template(
        self,
        recipient: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any]
    ) -> bool:
        """
        Send an email using a Jinja2 template.
        
        Args:
            recipient: Email address of recipient
            subject: Email subject line
            template_name: Name of template file (e.g., 'user_joined_group.html')
            context: Dictionary of variables for template rendering
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # TODO: Implement template-based email sending
        # Call render_template() to get html_body
        # Call send_email() with rendered content
        # Return result
        pass

    def test_connection(self) -> bool:
        """
        Test SMTP connection without sending an email.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        # TODO: Implement connection test
        # Connect to SMTP server
        # Call EHLO
        # Close connection
        # Return success boolean
        pass
