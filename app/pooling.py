import json

from utils.config import QUEUE_URL, sqs


def process_message(message_body):
    print(f"Processando mensagem: {message_body}")


def poll_sqs():
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
        )

        messages = response.get("Messages", [])

        if not messages:
            print("Nenhuma mensagem recebida, aguardando...")
            continue

        for message in messages:
            message_body = json.loads(message["Body"])
            process_message(message_body)

            sqs.delete_message(
                QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"]
            )
            print("Mensagem processada e removida da fila.")


if __name__ == "__main__":
    poll_sqs()
