import asyncio
from task.clients.client import DialClient
from task.clients.custom_client import DialClient as CustomClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool, custom: bool) -> None:

    print(f"Running in streaming:{stream} and custom:{custom} mode...\n")

    client = CustomClient(deployment_name="gpt-4") if custom else DialClient(deployment_name="gpt-4")
    conversation = Conversation()

    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    print("Provide System prompt or press 'enter' to continue.")
    system_prompt = input("System prompt>").strip() or DEFAULT_SYSTEM_PROMPT
    conversation.add_message(Message(Role.SYSTEM, system_prompt))

    print()

    # 4. Use infinite cycle (while True) and get yser message from console

    print("Type your question or 'exit' to quit.")
    while True:
        message = input(">")
        # 5. If user message is `exit` then stop the loop
        if message == "exit":
            print("Exiting the chat. Goodbye!")
            break

        # 6. Add user message to conversation history (role 'user')
        conversation.add_message(Message(Role.USER, message))
        # 7. If `stream` param is true -> call DialClient#stream_completion()
        if stream:
            response = await client.stream_completion(conversation.get_messages())
        else:
            response = client.get_completion(conversation.get_messages())

        conversation.add_message(response)

        # 9. Test it with DialClient and CustomDialClient
        # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response


asyncio.run(
    start(True, False)
)
