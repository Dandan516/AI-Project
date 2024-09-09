import gradio as gr
from gemini_ai import classify

interface = gr.Interface(
    fn=classify,
    inputs=["text"],
    outputs=["text"],
)

interface.launch()