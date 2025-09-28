from uagents import Agent, Protocol, Context
from pydantic import Field
from uagents.models import Model

class Message(Model):
    """A simple message model with a single text field."""
    text: str = Field(description="The content of the message.")


agent = Agent(
    name="alice",
    seed="alice_secret_seed_phrase",
)

chat_protocol = Protocol("SimpleChat")
@chat_protocol.on_message(model=Message, replies=Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    """
    Handles an incoming message, logs it, and sends a reply.

    Args:
        ctx: The agent's context, used for logging, storage, and sending messages.
        sender: The address of the agent that sent the message.
        msg: The message object that was received.
    """
    ctx.logger.info(f"Received message from agent with address: {sender}")
    ctx.logger.info(f"Message content: {msg.text}")

    response_text = f"Hello there! I received your message: '{msg.text}'"

    await ctx.send(sender, Message(text=response_text))
    ctx.logger.info(f"Sent reply to {sender}")

@agent.on_event("startup")
async def agent_startup(ctx: Context):
    """
    This function runs once when the agent starts.
    """
    ctx.logger.info(f"Agent '{ctx.name}' is starting up.")
    ctx.logger.info(f"My address is: {ctx.address}")
    ctx.logger.info("I am now ready to receive messages.")
    ctx.logger.info("You can send me a message from another agent or client.")

agent.include(chat_protocol)

if __name__ == "__main__":
    print("Starting agent 'alice'...")
    print("Press Ctrl+C to stop the agent.")
    agent.run()
