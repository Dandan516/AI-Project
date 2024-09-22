import time
import gradio as gr
from product_suggestion import find_products
from youtube_utils import summarize_channel_contents

def hide():
    return gr.update(visible=False)

def show():
    return gr.update(visible=True)

def show_if_not_empty(df: gr.Dataframe):
    if len(df.index) == 1:
        gr.Warning("No result!", duration=3)
        return hide()
    else:
        return show()

def switch_mode(choice):
    if choice == "Customer":   
        return gr.update(elem_classes="textbox", label="User prompt", placeholder="Type in what you need!")
    elif choice == "Youtuber":
        return gr.update(elem_classes="textbox", label="Channel URL", placeholder="Enter a YouTube channel URL.")

def get_result(user_input, mode):
    time.sleep(0.1)
    if mode == "Customer":
        return find_products(user_input)
    elif mode == "Youtuber":
        channel_content_summary = summarize_channel_contents(user_input)
        return find_products(channel_content_summary)

with gr.Blocks() as interface: 
    gr.Markdown("Product suggestion AI")
    mode = gr.Radio(choices = ["Customer", "Youtuber"], label = "Mode")
    user_input = gr.Textbox(visible=False)
    run_btn = gr.Button(value="Run", visible=False)
    
    mode.select(fn=switch_mode, inputs=mode, outputs=user_input)
    mode.change(fn=show, outputs=user_input)
    mode.change(fn=show, outputs=run_btn)
    
    result = gr.Dataframe(height=800, row_count=1, visible=False, interactive=False)
    run_btn.click(fn=get_result, inputs=[user_input, mode], outputs=result)
    run_btn.click(fn=show_if_not_empty, inputs=result, outputs=result)

interface.launch()