import requests
from typing import Dict
from logger import logger

def send_webhook_notification(webhook_url: str, payload: Dict) -> None:
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Webhook notification sent successfully")
    except requests.RequestException as e:
        logger.error(f"Failed to send webhook notification: {e}")
