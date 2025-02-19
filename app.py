import gradio as gr
from state import State
from const import *

state = State(DEFAULT_MODEL_1, DEFAULT_MODEL_2)

# def update_entry_id(entry_id):
#     num_turn_1, num_turn_2, processed_step_response_1, processed_step_response_2 = state.update_entry(entry_id)
#     return processed_step_response_1, processed_step_response_2, f"{0}/{state.max_num_turn}"

# Function to update entry ID based on button clicks
def update_entry_id(current_id, change):
    new_id = max(0, min(199, current_id + change))
    return new_id

# Function to update entry ID from text field
def set_entry_id(entry_text):
    try:
        entry_id = int(entry_text)
        return max(0, min(199, entry_id))  # Ensure it's within range
    except ValueError:
        return 0  # Default to 0 if input is invalid
  
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
    gr.Markdown("# LLM Judge")
    with gr.Tabs():
        ### Page 1: LLM Judge Analysis and Visualization
        with gr.Tab("LLM Judge - Analysis"):
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
                entry_id = gr.Slider(
                    minimum=0,
                    maximum=199,
                    step=1,
                    label="Entry ID",
                    value=0
                )

            with gr.Row():
                model_1 = gr.Dropdown(
                    choices=MODELS,
                    label="Model 1",
                    value='gpt-4o-2024-08-06-FC', 
                )
                model_2 = gr.Dropdown(
                    choices=MODELS, 
                    label="Model 2",
                    value='meta-llama_Llama-3.1-8B-Instruct', 
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
                prev_btn = gr.Button("Previous")
                entry_text = gr.Textbox(value="0", label="Entry ID")
                next_btn = gr.Button("Next")

            # Update entry ID on button clicks
            prev_btn.click(update_entry_id, [entry_text, gr.Number(-1)], entry_text)
            next_btn.click(update_entry_id, [entry_text, gr.Number(1)], entry_text)

            # Update entry ID from text input
            entry_text.submit(set_entry_id, entry_text, entry_text)
                
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