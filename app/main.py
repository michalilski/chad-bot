import gradio as gr
import pandas as pd

from app.core.chat import DialogueLoop
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.nlg.nlg import NLG
from app.core.db.db_bridge import DatabaseBridge


def build_chatbot(nlg: NLG):
    dialogue_loop: DialogueLoop = DialogueLoop(
        DSTModule(),
        ChatGPTBasedIntentDetectionModule(),
        nlg,
    )

    def get_all_tickets_df():
        return pd.DataFrame.from_records([ticket.to_dict() for ticket in DatabaseBridge.get_all_bookings()])

    def respond(message, chat_history):
        bot_message = dialogue_loop.step(message)
        chat_history.append((message, bot_message))
        return "", chat_history, get_all_tickets_df()

    chatbot = gr.Chatbot()
    chatbot.style(height=750)
    msg = gr.Textbox(label="Input")
    clear = gr.Button("Clear")
    gr.Label("Behind The Scenes", label=None)
    gr_tickets_table = gr.Dataframe(
        row_count=(1, "dynamic"),
        col_count=(3, "fixed"),
        label="Tickets in database",
        headers=["movie", "date", "4_digit_pin"],
        value=get_all_tickets_df(),
    )

    msg.submit(respond, [msg, chatbot], [msg, chatbot, gr_tickets_table])
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
