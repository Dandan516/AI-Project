import gradio as gr
import pandas as pd
import time
from product_suggestion import find_products

def show_outputs():
    return gr.update(visible=True)

def get_result(input):
    time.sleep(0.1)
    return find_products(input)

with gr.Blocks() as interface:
    gr.Markdown("Product suggestion AI")
    user_input = gr.Textbox(placeholder="I want to go hiking.")
    btn = gr.Button(value="Run")
    result = gr.Dataframe(visible=False, interactive=False)
    btn.click(fn=show_outputs, outputs=result)
    btn.click(fn=get_result, inputs=user_input, outputs=result)

interface.launch()