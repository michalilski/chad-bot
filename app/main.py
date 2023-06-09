import base64
from pathlib import Path

import gradio as gr
import pandas as pd
import soundfile as sf
from TTS.api import TTS
from freezegun import freeze_time

from app.core.chat import DialogueLoop
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import ChatGPTBasedIntentDetectionModule
from app.core.chat.nlg.nlg import NLG
from app.core.db.db_bridge import DatabaseBridge

_tts = None
dialogue_loop: DialogueLoop = None
INITIAL_TURN = [("Hi!", "Hello, my name is Todd, a cinema bot. How can i help you?")]


def get_tts():
    global _tts
    if _tts is None:
        _tts = TTS(
            model_name="tts_models/en/ljspeech/tacotron2-DDC",
            vocoder_path="vocoder_models/en/sam/hifigan_v2",
            progress_bar=True,
            gpu=True,
        )
    return _tts


audio_output_path = Path("data/audio") / "generated_response_audio.wav"


def build_chatbot(nlg: NLG):
    def setup_loop():
        global dialogue_loop
        dialogue_loop = DialogueLoop(
            DSTModule(),
            ChatGPTBasedIntentDetectionModule(),
            nlg,
        )
        DatabaseBridge.setup_example_bookings()
        return INITIAL_TURN, get_all_tickets_df()

    def get_all_tickets_df():
        return pd.DataFrame.from_records([ticket.to_dict() for ticket in DatabaseBridge.get_all_bookings()])

    def text_to_speech_html(text):
        try:
            audio = get_tts().tts(text=text)
            sf.write(audio_output_path, audio, samplerate=22_050)

            with audio_output_path.open("rb") as audio_output_file:
                audio = base64.b64encode(audio_output_file.read()).decode("utf-8")

            audio_player = f'<audio src="data:audio/mpeg;base64,{audio}" controls autoplay></audio>'
            return audio_player
        except:
            return ""

    def get_state():
        return dialogue_loop._current_state.to_dataframe()

    def respond(message, chat_history):
        bot_response = dialogue_loop.step(message)
        chat_history.append((message, bot_response))
        return "", chat_history, get_all_tickets_df(), text_to_speech_html(bot_response), get_state()

    setup_loop()
    chatbot = gr.Chatbot(value=INITIAL_TURN)
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

    audio_html = gr.HTML()
    audio_html.visible = False

    state_table = gr.DataFrame(
        row_count=(1, "dynamic"),
        col_count=(2, "fixed"),
        label="Dialogue state",
        headers=["Slot", "Value"],
        value=get_state(),
    )

    msg.submit(respond, [msg, chatbot], [msg, chatbot, gr_tickets_table, audio_html, state_table])
    clear.click(setup_loop, None, [chatbot, gr_tickets_table], queue=False)


def update_nlg_style(nlg: NLG, nlg_style: str):
    print(f"updating nlg style to {nlg_style}")
    nlg.style = nlg_style


with freeze_time("2023-07-01"):
    with gr.Blocks() as demo:
        nlg = NLG()
        nlg_styles = list(nlg.PROMPTS_WITH_USER_MESSAGE.keys())
        dropdown = gr.Dropdown(nlg_styles, value=nlg_styles[0], label="Response style")
        dropdown.change(fn=lambda nlg_style: update_nlg_style(nlg, nlg_style), inputs=[dropdown])
        build_chatbot(nlg)
        demo.launch(
            server_name="0.0.0.0", debug=True, prevent_thread_lock=False, inbrowser=False, ssl_verify=False
        )  # share=True when app is ready
