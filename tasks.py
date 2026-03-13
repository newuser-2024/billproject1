import os
import logging
from celery import Celery
from celery.utils.log import get_task_logger
from typing import List, Dict, Any

# Configure Celery
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery(__name__, broker=redis_url, backend=redis_url)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

logger = get_task_logger(__name__)


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def send_join_notification(self, user_id: int, group_id: int):
    """
    Background task: Send email notification when a user joins a group.
    
    Args:
        user_id: ID of user who joined
        group_id: ID of group they joined
        
    Retries:
        Max 3 attempts with 60 second backoff between retries
    """
    try:
        # TODO: Implement join notification task
        # 1. Check user preferences: notify_on_join should be True
        # 2. Query database for user who joined (name, email)
        # 3. Query database for group info (name, group_id)
        # 4. Query database for other group members (emails)
        # 5. Render 'user_joined_group.html' template with context:
        #    - joiner_name
        #    - group_name
        #    - group_id (for action link)
        # 6. Loop through recipient emails
        # 7. For each recipient, call EmailService.send_email_with_template()
        # 8. Log to notification_log table: user_id, event_type='join', status='sent'
        # 9. Call track_event('notification.sent', {...})
        # 10. Return success message
        logger.info(f"Queued join notification for user {user_id} in group {group_id}")
    except Exception as exc:
        logger.error(f"Error sending join notification: {exc}")
        # TODO: Track event: notification.failed
        raise self.retry(exc=exc, countdown=60)


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def send_expense_notification(self, expense_id: int, group_id: int):
    """
    Background task: Send email notification when an expense is added to a group.
    
    Args:
        expense_id: ID of expense that was added
        group_id: ID of group the expense belongs to
        
    Retries:
        Max 3 attempts with 60 second backoff between retries
    """
    try:
        # TODO: Implement expense notification task
        # 1. Query expense record by expense_id
        # 2. Query payer user info (name, email)
        # 3. Query group info (name)
        # 4. For each group member with notify_on_expense=True:
        #    a. Check user preference before sending
        #    b. Render 'expense_added.html' template with context:
        #       - payer_name
        #       - amount (formatted as currency)
        #       - description
        #       - group_name
        #       - group_id (for action link)
        #    c. Send email via EmailService
        #    d. Log to notification_log: event_type='expense', status='sent'
        # 5. Call track_event('notification.sent', {...})
        # 6. Return success message
        logger.info(f"Queued expense notification for expense {expense_id} in group {group_id}")
    except Exception as exc:
        logger.error(f"Error sending expense notification: {exc}")
        # TODO: Track event: notification.failed
        raise self.retry(exc=exc, countdown=60)


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def send_settlement_notification(self, transactions: List[Dict[str, Any]], group_id: int):
    """
    Background task: Send email notification for settlement transactions.
    
    Args:
        transactions: List of transaction dicts with keys:
            - debtor_user_id: User who owes money
            - creditor_user_id: User who is owed money
            - amount: Amount owed
        group_id: ID of group these transactions belong to
        
    Retries:
        Max 3 attempts with 60 second backoff between retries
    """
    try:
        # TODO: Implement settlement notification task
        # 1. For each transaction in transactions list:
        #    a. Get debtor user (name, email)
        #    b. Get creditor user (name, email)
        #    c. Check both users' notify_on_settlement preference
        #    d. If debtor notify=True, send settlement email:
        #       - Render 'settlement_required.html' with context:
        #         - debtor_name
        #         - creditor_name
        #         - amount
        #         - group_name
        #         - group_id (for action link)
        #       - Send to debtor_email
        #       - Log to notification_log: event_type='settlement', status='sent'
        # 2. Call track_event('notification.sent', {...}) for each sent email
        # 3. Return summary: "Sent X settlement notifications"
        logger.info(f"Queued settlement notifications for {len(transactions)} transactions in group {group_id}")
    except Exception as exc:
        logger.error(f"Error sending settlement notification: {exc}")
        # TODO: Track event: notification.failed
        raise self.retry(exc=exc, countdown=60)


@celery.task(bind=True, max_retries=1)
def log_notification_event(self, user_id: int, event_type: str, status: str = "pending"):
    """
    Background task: Log a notification event to the audit trail.
    
    Args:
        user_id: ID of user receiving notification
        event_type: Type of event ('join', 'expense', 'settlement')
        status: Status of notification ('pending', 'sent', 'failed')
    """
    try:
        # TODO: Implement notification logging
        # INSERT into notification_log table:
        # - user_id
        # - event_type
        # - status
        # - sent_at (current timestamp)
        logger.info(f"Logged {event_type} notification for user {user_id} with status {status}")
    except Exception as exc:
        logger.error(f"Error logging notification event: {exc}")
        raise self.retry(exc=exc, countdown=10)
