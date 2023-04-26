import gradio as gr

from app.core.chat import chatgpt_based_dialogue_handler


def respond(message, chat_history):
    bot_message = chatgpt_based_dialogue_handler.answer(chat_history, message)
    chat_history.append((message, bot_message))
    return "", chat_history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(server_port=8000, debug=True)  # share=True when app is ready