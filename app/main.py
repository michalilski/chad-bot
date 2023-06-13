import gradio as gr

from app.core.chat import ChatGPTBridge, DialogueLoop
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.nlg.nlg import NLG

with gr.Blocks() as demo:
    dialogue_loop: DialogueLoop = DialogueLoop(
        DSTModule(),
        ChatGPTBasedIntentDetectionModule(),
        NLG(),
    )

    def respond(message, chat_history):
        bot_message = dialogue_loop.step(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    chatbot = gr.Chatbot()
    chatbot.style(height=750)
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(
    server_name="0.0.0.0", debug=True, prevent_thread_lock=False, inbrowser=False, ssl_verify=False
)  # share=True when app is ready
