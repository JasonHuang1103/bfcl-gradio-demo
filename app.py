import gradio as gr
import plotly.graph_objects as go
import random
from state import State
from const import *

state = State(DEFAULT_MODEL_1, DEFAULT_MODEL_2)

def create_doughnut_chart():
    # Create data for doughnut chart with random values
    labels = ['Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7']
    values = [random.randint(10, 100) for _ in range(7)]  # Random values between 10 and 100
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        textinfo='label+percent',
        textposition='outside',
        showlegend=False,
        marker=dict(
            colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', '#FFB366']  # Custom colors
        )
    )])
    
    fig.update_layout(
        width=1000,
        height=800,
        title={
            'text': "Data Distribution by Field",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        annotations=[{
            'text': 'Total Fields: 7',
            'x': 0.5,
            'y': 0.5,
            'font_size': 20,
            'showarrow': False
        }]
    )
    return fig

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

def update_sunburst(temp1, temp2, temp3, temp4, temp5, temp6, temp7):
    # Update the doughnut chart based on slider values
    labels = ['temp1', 'temp2', 'temp3', 'temp4', 'temp5', 'temp6', 'temp7']
    values = [temp1, temp2, temp3, temp4, temp5, temp6, temp7]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        textinfo='label+percent',
        textposition='outside',
        showlegend=False
    )])
    
    fig.update_layout(
        width=800,
        height=800,
        title={
            'text': "Dataset Distribution",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig

with gr.Blocks() as demo:
    with gr.Tabs() as tabs:
        # Homepage
        with gr.Tab("Home"):
            gr.Markdown("# Welcome to BFCL V3")
            
            # Main image at the top
            image_input = gr.Image(
                value="./images/main",
                label="Main Image",
                type="filepath",
                height=500,
                interactive=False,  # Make it non-interactive
                show_label=False    # Hide the label since it's the main hero image
            )
            
            # Text input below image
            text_input = gr.Textbox(
                label="Search",
                placeholder="Search...",
                lines=1,
                show_label=False
            )
            
            # Navigation section
            gr.Markdown("## Quick Navigation")
            with gr.Row():
                with gr.Column(scale=1):
                    model_comp_btn = gr.Button("Model Comparison", size="large")
                with gr.Column(scale=1):
                    dataset_exp_btn = gr.Button("Dataset Explorer", size="large")
                with gr.Column(scale=1):
                    metrics_btn = gr.Button("Metrics Dashboard", size="large")
                with gr.Column(scale=1):
                    analysis_btn = gr.Button("Analysis Tools", size="large")
            
            # Additional row of navigation buttons
            with gr.Row():
                with gr.Column(scale=1):
                    docs_btn = gr.Button("Documentation", size="large")
                with gr.Column(scale=1):
                    settings_btn = gr.Button("Settings", size="large")
                with gr.Column(scale=1):
                    about_btn = gr.Button("About", size="large")
            
            # Spacing
            gr.Markdown("<br>")
            
            # Additional image spaces
            gr.Markdown("## Featured")
            image_space_1 = gr.Image(
                value="./images/img1",
                label="Featured Image 1",
                type="filepath",
                height=500,
                interactive=False,
                show_label=False
            )
            
            image_space_2 = gr.Image(
                value="./images/img2",
                label="Featured Image 2",
                type="filepath",
                height=500,
                interactive=False,
                show_label=False
            )
            
            image_space_3 = gr.Image(
                value="./images/img3",
                label="Featured Image 3",
                type="filepath",
                height=500,
                interactive=False,
                show_label=False
            )

        # Model Comparison Page
        with gr.Tab("Model Comparison", id="model_comparison"):
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

        # Dataset Explorer Page
        with gr.Tab("Dataset Explorer", id="dataset_explorer"):
            gr.Markdown("# Dataset Explorer")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    ## Field Distribution
                    This chart shows the distribution of data across different fields.
                    Each segment represents a field's proportion in the dataset.
                    """)
                    plot = gr.Plot(value=create_doughnut_chart())

    # Event handlers for model comparison page
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

    # Navigation button handlers
    model_comp_btn.click(fn=lambda: gr.Tabs(selected="model_comparison"), outputs=tabs)
    dataset_exp_btn.click(fn=lambda: gr.Tabs(selected="dataset_explorer"), outputs=tabs)

    # Additional navigation button handlers
    metrics_btn.click(fn=lambda: gr.Tabs(selected="model_comparison"), outputs=tabs)  # Temporarily pointing to model comparison
    analysis_btn.click(fn=lambda: gr.Tabs(selected="dataset_explorer"), outputs=tabs)  # Temporarily pointing to dataset explorer
    docs_btn.click(fn=lambda: gr.Tabs(selected="home"), outputs=tabs)
    settings_btn.click(fn=lambda: gr.Tabs(selected="home"), outputs=tabs)
    about_btn.click(fn=lambda: gr.Tabs(selected="home"), outputs=tabs)

if __name__ == "__main__":
    demo.launch(share=True)