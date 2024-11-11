from collections import deque

from main import start_audit

import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    messages = cl.user_session.get("messages") if cl.user_session.get("messages") else deque(maxlen=5)
    messages = messages + deque(["User: " + message.content])
    async for part in start_audit(messages=messages):
        await msg.stream_token(part)

    cl.user_session.set("messages", messages)
    await msg.update()


@cl.on_chat_start
async def on_chat_start():
    content = (
        "Hello, I'm Energemin, your energy efficiency assistant, "
        "please ask me anything about your machine energy efficiency."
    )
    await cl.Message(content=content, author="Energemin").send()
