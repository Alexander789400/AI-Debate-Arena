import gradio as gr
import time
import asyncio
import sys

from graph.debate_graph import run_debate
from tools.tts import speak


# Fix Windows async bug
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Typing animation + speech
def stream_and_speak(text, agent):

    audio = speak(text, agent)
    typed = ""

    for c in text:
        typed += c
        time.sleep(0.02)
        yield typed, audio


def start_debate(topic):

    try:
        
        # show immediate response
        yield "", "", "⏳ Preparing debate agents...", "Starting Debate", None
        
        transcript, final = run_debate(topic)

        for r in transcript:

            # PRO
            for text, audio in stream_and_speak(r["pro"], "pro"):
                yield (
                    text + "<script>talk('pro_avatar')</script>",
                    "",
                    "",
                    f"### Round {r['round']}",
                    audio
                )

            time.sleep(1)

            # CON
            for text, audio in stream_and_speak(r["con"], "con"):
                yield (
                    "",
                    text + "<script>talk('con_avatar')</script>",
                    "",
                    f"### Round {r['round']}",
                    audio
                )

            time.sleep(1)

            # JUDGE
            for text, audio in stream_and_speak(r["judge"], "judge"):
                yield (
                    "",
                    "",
                    text + "<script>talk('judge_avatar')</script>",
                    f"### Round {r['round']}",
                    audio
                )

            time.sleep(1)

        # FINAL RESULT
        for text, audio in stream_and_speak(final, "judge"):
            yield (
                "",
                "",
                text + "<script>talk('judge_avatar')</script>",
                "## 🏆 Final Decision",
                audio
            )

    except Exception as e:
        print("Debate error:", e)
        yield "", "", f"❌ Error: {str(e)}", "Error", None


with gr.Blocks(css="ui/style.css") as demo:

    gr.Markdown("# 🎤 AI Debate Arena")

    # Talking animation script
    gr.HTML("""
    <script>
    function talk(id){
        let avatar = document.getElementById(id);
        if(avatar){
            avatar.classList.add("talking");
            setTimeout(()=>avatar.classList.remove("talking"),2500);
        }
    }
    </script>
    """)

    topic = gr.Textbox(label="Debate Topic")

    start = gr.Button("Start Debate")

    round_box = gr.Markdown()

    audio_player = gr.Audio(autoplay=True)

    with gr.Row():

        # PRO
        with gr.Column():
            gr.Markdown("## 🟢 PRO AGENT")
            gr.Image(
                value="ui/avatars/pro.png",
                height=150,
                elem_id="pro_avatar",
                show_label=False
            )
            pro_box = gr.Markdown()

        # JUDGE
        with gr.Column():
            gr.Markdown("## ⚖️ JUDGE AGENT")
            gr.Image(
                value="ui/avatars/judge.png",
                height=150,
                elem_id="judge_avatar",
                show_label=False
            )
            judge_box = gr.Markdown()

        # CON
        with gr.Column():
            gr.Markdown("## 🔴 CON AGENT")
            gr.Image(
                value="ui/avatars/con.jpg",
                height=150,
                elem_id="con_avatar",
                show_label=False
            )
            con_box = gr.Markdown()

    start.click(
        start_debate,
        inputs=topic,
        outputs=[
            pro_box,
            con_box,
            judge_box,
            round_box,
            audio_player
        ]
    )


demo.launch(
    server_port=7860,
    share=False
)