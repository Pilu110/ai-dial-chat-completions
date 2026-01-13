import asyncio
from task.clients.client import DialClient
from task.clients.custom_client import DialClient as CustomClient
from task.constants import DEFAULT_SYSTEM_PROMPT, API_KEY
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:

    #TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    client = DialClient(deployment_name="gpt-4", api_key=API_KEY)

    # 1.2. Create CustomDialClient
    # custom_client = CustomClient(deployment_name="custom")

    # 2. Create Conversation object
    conversation = Conversation()

    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    print("Provide System prompt or press 'enter' to continue.")
    system_prompt = input(">") or DEFAULT_SYSTEM_PROMPT
    conversation.add_message(Message(Role.SYSTEM, system_prompt))

    # 4. Use infinite cycle (while True) and get yser message from console

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
            await client.stream_completion(conversation.get_messages())
        else:
            client.get_completion(conversation.get_messages())
        #    else -> call DialClient#get_completion()
        # 8. Add generated message to history
        # 9. Test it with DialClient and CustomDialClient
        # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response
        raise NotImplementedError


asyncio.run(
    start(True)
)
