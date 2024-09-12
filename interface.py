import gradio as gr
import pandas as pd
from gemini_ai import match

interface = gr.Interface(
    title="Product suggestion AI",
    description="Tell our AI what you need!", 
    fn=match,
    inputs="text",
    outputs="text",
)

interface.launch()