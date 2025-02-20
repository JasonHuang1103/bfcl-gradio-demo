import gradio as gr
from state import State
from const import *

state = State(DEFAULT_MODEL_1, DEFAULT_MODEL_2)

def update_entry_id(entry_id):
    error_info_1, error_info_2 = state.update_entry(entry_id)
    # Format the display for each model
    display_1 = [
        ["Error Type:", error_info_1['type']],
        ["Error Description:", error_info_1['description']],
        ["Turn ID:", str(error_info_1['turn_id'])]
    ]
    display_2 = [
        ["Error Type:", error_info_2['type']],
        ["Error Description:", error_info_2['description']],
        ["Turn ID:", str(error_info_2['turn_id'])]
    ]
    return display_1, display_2

def update_model(model1, model2):
    state.update_model(model1, model2)
    display_1, display_2 = update_entry_id(entry_id=0)
    return display_1, display_2, 0

def initialize():
    print("Initializing...")
    return update_entry_id(entry_id=0)

with gr.Blocks() as demo:
    gr.Markdown("# BFCL V3")
    with gr.Tabs():
        ### Page 1: LLM Judge Output Result Dataset
        with gr.Tab("LLM Judge - Dataset"):
            gr.Markdown("# LLM Judge")
            gr.Markdown("## Introduction")
            gr.Markdown("## Dataset statistics")          
        
        ### Page 2: Metrics and Visualization
        with gr.Tab("Metrics and Visualizations"):
            gr.Markdown("# Metrics visualization and discussion")
            
        ### Page 3: Comparison of two different models
        with gr.Tab("Compare LLM Performance"):
            gr.Markdown("# Compare LLM Performance")
            
            with gr.Row():
                model_1 = gr.Dropdown(
                    choices=MODELS,
                    label="Model 1",
                    value=DEFAULT_MODEL_1
                )
                model_2 = gr.Dropdown(
                    choices=MODELS, 
                    label="Model 2",
                    value=DEFAULT_MODEL_2
                )
            
            initial_display_1, initial_display_2 = initialize()
            with gr.Row():
                chatbot_1 = gr.Dataframe(
                    value=initial_display_1,
                    headers=["Field", "Value"],
                    label="Model 1 Error Analysis"
                )
                chatbot_2 = gr.Dataframe(
                    value=initial_display_2,
                    headers=["Field", "Value"],
                    label="Model 2 Error Analysis"
                )
                     
            with gr.Row(equal_height=True, scale=0.6):
                prev_entry_button = gr.Button("Previous Entry")
                entry_id = gr.Number(
                    minimum=0,
                    maximum=199,
                    label="Entry ID",
                    value=0,
                    interactive=True,
                )
                next_entry_button = gr.Button("Next Entry")

            def update_entry_buttons(entry_id, increase=True):
                new_entry_id = int(entry_id)
                if increase:
                    new_entry_id = min(new_entry_id + 1, 199)
                else:
                    new_entry_id = max(new_entry_id - 1, 0)
                display_1, display_2 = update_entry_id(new_entry_id)
                return display_1, display_2, new_entry_id
            
            prev_entry_button.click(
                fn=lambda entry_id: update_entry_buttons(entry_id, False),
                inputs=[entry_id],
                outputs=[chatbot_1, chatbot_2, entry_id]
            )
            
            next_entry_button.click(
                fn=lambda entry_id: update_entry_buttons(entry_id, True),
                inputs=[entry_id],
                outputs=[chatbot_1, chatbot_2, entry_id]
            )
                
            entry_id.change(
                fn=update_entry_id,
                inputs=[entry_id],
                outputs=[chatbot_1, chatbot_2]
            )
            
            model_1.change(
                fn=update_model,
                inputs=[model_1, model_2],
                outputs=[chatbot_1, chatbot_2, entry_id]
            )
            
            model_2.change(
                fn=update_model,
                inputs=[model_1, model_2],
                outputs=[chatbot_1, chatbot_2, entry_id]
            )

if __name__ == "__main__":
    demo.queue()
    demo.launch(share=True)