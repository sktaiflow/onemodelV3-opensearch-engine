from airflow.models import Variable
from airflow.providers.sktvane.macros.slack_notifier import SlackNotifier


def get_slack_notifier(slack_email: str) -> SlackNotifier:
    return SlackNotifier(
        slack_channel="#test-channel",
        slack_username=f"Airflow-AlarmBot",
        slack_email=slack_email,
    )
