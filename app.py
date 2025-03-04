import gradio as gr
from state import State
from const import *

state = State(DEFAULT_MODEL_1, DEFAULT_MODEL_2)

def update_entry_id(entry_id):
    num_turn_1, num_turn_2, processed_step_response_1, processed_step_response_2 = state.update_entry(entry_id)
    return processed_step_response_1, processed_step_response_2, f"{0}/{state.max_num_turn}"
  
def update_turn_id(entry_id, turn_id, increase=True):
    turn_id = int(turn_id[0])
    if increase:
        turn_id = min(turn_id + 1, state.max_num_turn)
    else:
        turn_id = max(turn_id - 1, 0)
    processed_step_response_1, processed_step_response_2 = state.update_turn(entry_id, turn_id)
    return processed_step_response_1, processed_step_response_2, f'{turn_id}/{state.max_num_turn}'

def update_model(model1, model2):
    state.update_model(model1, model2)
    processed_step_response_1, processed_step_response_2, turn_id_display = update_entry_id(entry_id=0)
    return processed_step_response_1, processed_step_response_2, turn_id_display, 0

def initialize():
    print("Initializing...")
    _, _, initial_processed_step_response_1, initial_processed_step_response_2 = state.update_entry(entry_id=0)
    return initial_processed_step_response_1, initial_processed_step_response_2, f'{0}/{state.max_num_turn}'

with gr.Blocks() as demo:
    gr.Markdown("# BFCL V3")
    with gr.Tabs():
        ### Page 1: This page contains the description of the BFCL-V3 dataset and visualizations
        with gr.Tab("BFCL V3 - Dataset"):
            gr.Markdown("# The Berkeley Function-Calling Leaderboard (BFCL) V3")
            gr.Markdown("## Introduction")
            gr.Markdown("## Dataset statistics")          
        
        ### Page 2: This page contains the description of metrics and visualizations on each models
        with gr.Tab("Metrics and Visualizations"):
            gr.Markdown("# Metrics visualization and discussion")
            
        ### Page 3: This page contains the comparison of two different models
        with gr.Tab("Compare LLM Performance"):
            gr.Markdown("# Compare LLM Performance")
            
            with gr.Row():
                model_1 = gr.Dropdown(
                    choices=MODELS,
                    label="Model 1",
                    value='gpt-4o-2024-11-20-FC',
                )
                model_2 = gr.Dropdown(
                    choices=MODELS, 
                    label="Model 2",
                    value='DeepSeek-V3-FC',
                )
            
            initial_chatbot_1, initial_chatbot_2, initial_turn_id_display = initialize()
            with gr.Row():
                chatbot_1 = gr.Chatbot(
                    value=initial_chatbot_1, 
                    label="Model 1 Conversation"
                )
                chatbot_2 = gr.Chatbot(
                    value=initial_chatbot_2, 
                    label="Model 2 Conversation"
                )
                
            with gr.Row(equal_height=True):
                prev_turn_button = gr.Button("Previous Turn")
                turn_id_display = gr.Textbox(
                    value=initial_turn_id_display,
                    label="Current Turn ID / Total Turn",
                    interactive=False,
                    elem_id="turn_id_display",
                    lines=1,
                )
                next_turn_button = gr.Button("Next Turn")
                     
            with gr.Row():
                entry_id = gr.Slider(
                    minimum=0,
                    maximum=199,
                    step=1,
                    label="Entry ID",
                    value=0
                )
                
            with gr.Row():
                text_output_1 = gr.Textbox(label="Model 1 Metrics", interactive=False)
                text_output_2 = gr.Textbox(label="Model 2 Metrics", interactive=False)
                
            prev_turn_button.click(
                fn=lambda entry_id, turn_id_display: update_turn_id(entry_id, turn_id_display, False),
                inputs=[entry_id, turn_id_display],
                outputs=[chatbot_1, chatbot_2, turn_id_display]
            )
            
            next_turn_button.click(
                fn=lambda entry_id, turn_id_display: update_turn_id(entry_id, turn_id_display, True),
                inputs=[entry_id, turn_id_display],
                outputs=[chatbot_1, chatbot_2, turn_id_display]
            )
                
            entry_id.change(
                fn=update_entry_id,
                inputs=[entry_id],
                outputs=[chatbot_1, chatbot_2, turn_id_display]
            )
            
            model_1.change(
                fn=update_model,
                inputs=[model_1, model_2],
                outputs=[chatbot_1, chatbot_2, turn_id_display, entry_id]
            )
            
            model_2.change(
                fn=update_model,
                inputs=[model_1, model_2],
                outputs=[chatbot_1, chatbot_2, turn_id_display, entry_id]
            )

if __name__ == "__main__":
    demo.launch(share=True)