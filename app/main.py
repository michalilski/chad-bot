import gradio as gr

from app.core.chat import DialogueLoop
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.nlg.nlg import NLG


def build_chatbot(nlg: NLG):
    dialogue_loop: DialogueLoop = DialogueLoop(
        DSTModule(),
        ChatGPTBasedIntentDetectionModule(),
        nlg,
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


def update_nlg_style(nlg: NLG, nlg_style: str):
    print(f"updating nlg style to {nlg_style}")
    nlg.style = nlg_style


with gr.Blocks() as demo:
    nlg = NLG()
    nlg_styles = list(nlg.PROMPTS_WITH_USER_MESSAGE.keys())
    dropdown = gr.Dropdown(nlg_styles, value=nlg_styles[0], label="Response style")
    dropdown.change(fn=lambda nlg_style: update_nlg_style(nlg, nlg_style), inputs=[dropdown])
    build_chatbot(nlg)
    demo.launch(
        server_name="0.0.0.0", debug=True, prevent_thread_lock=False, inbrowser=False, ssl_verify=False
    )  # share=True when app is ready
