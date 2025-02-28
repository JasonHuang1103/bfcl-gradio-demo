import gradio as gr
import random
import json
import pandas as pd
from standardize import get_result
from const import *

class State:
    def __init__(self, model_name_1, model_name_2):
        self.model_name_1 = model_name_1
        self.model_name_2 = model_name_2
        self.result_1 = None
        self.result_2 = None
        self.max_num_turn = None
        self.update_model(model_name_1, model_name_2)

    def update_model(self, model_name_1, model_name_2):
        """
        Takes in the models names and updates the state, including
        * result 
        """
        model_1_path = f'{RESULT_PATH}/{model_name_1}/BFCL_v3_multi_turn_base_result.json'
        model_2_path = f'{RESULT_PATH}/{model_name_2}/BFCL_v3_multi_turn_base_result.json'
        self.model_name_1 = model_name_1
        self.model_name_2 = model_name_2
        self.result_1 = get_result(model_1_path)
        self.result_2 = get_result(model_2_path)
    
    def update_result(self):
        """
        Called after update_model, updates the result dataframe for both models
        """
        pass
      
    def update_entry(self, entry_id):
        """
        Takes in the entry id and updates the state
        """
        entry_1 = self.result_1.iloc[entry_id]
        entry_2 = self.result_2.iloc[entry_id]
        
        num_turn_1 = len(entry_1['result'])
        num_turn_2 = len(entry_2['result'])
        
        self.max_num_turn = max(num_turn_1, num_turn_2)
        self.current_entry_id = entry_id
        self.current_turn_id = 0
        self.current_step_id = 0
        
        step_response_1 = self.get_step_response(entry_1, 0, 0)
        step_response_2 = self.get_step_response(entry_2, 0, 0)
        
        # Return empty list if no responses
        processed_step_response_1 = step_response_1 if step_response_1 else []
        processed_step_response_2 = step_response_2 if step_response_2 else []
        
        return num_turn_1, num_turn_2, processed_step_response_1, processed_step_response_2

    def get_step_response(self, entry, turn_id, step_id):
        """
        Helper function to get the step response
        """
        try:
            if turn_id >= len(entry['result']):
                return None
            
            turn_response = entry['result'][turn_id]
            if isinstance(turn_response, list):
                # Handle tool responses (which are dictionaries) and text responses
                tool_responses = [resp for resp in turn_response if isinstance(resp, dict)]
                text_response = next((resp for resp in turn_response if isinstance(resp, str)), None)
                
                # Return in the format expected by chatbot
                return [("User", text_response if text_response else "No user message"), 
                       ("Assistant", self.format_tool_responses(tool_responses))]
            return None
        except Exception as e:
            print(f"Error getting step response: {str(e)}")
            return None

    def format_tool_responses(self, tool_responses):
        """
        Format tool responses into a single string
        """
        response = ""
        for tool_response in tool_responses:
            if isinstance(tool_response, dict) and 'content' in tool_response:
                content = tool_response['content']
                if content is not None:
                    response += content + "\n"
        return response if response else "No response"

    def get_processed_step_response(self, entry_id, turn_id):
        """
        Return the processed step response for a given entry and turn index.
        The processed step response is a list of tuples, so that the gradio chatbot can render it.
        """
        user_response_1 = self.result_1.iloc[entry_id]['turn_responses'][turn_id]['turn_eval_message'][-1]
        assistant_response_1 = self.result_1.iloc[entry_id]['turn_responses'][turn_id]['step_responses']
        user_response_2 = self.result_2.iloc[entry_id]['turn_responses'][turn_id]['turn_eval_message'][-1]
        assistant_response_2 = self.result_2.iloc[entry_id]['turn_responses'][turn_id]['step_responses']
        return self.get_process_step_response_helper(user_response_1, assistant_response_1), self.get_process_step_response_helper(user_response_2, assistant_response_2)
      
    def get_process_step_response_helper(self, user_response, assistant_responses):
        """
        Helper function to process the step response
        """
        processed_step_response = []
        processed_step_response.append((user_response['content'], None))
        for assistant_response in assistant_responses:
            processed_step_response.append((None, self.format_step_response(assistant_response)))
        return processed_step_response
    
    def format_step_response(self, step_response):
        """
        Helper function to process the step response
        """
        assert {'assistant_response', 'handler_response', 'tool_response'}.issubset(step_response.keys())
        step_response_processed = ""
        step_response_processed += "<b>Model Response🤖: </b><br>" 
        
        # Handle case where handler_response is None
        if step_response['handler_response'] is None:
            # Handle case where assistant_response is None
            assistant_response = step_response['assistant_response']
            if assistant_response is not None:
                step_response_processed += assistant_response + "\n"
            else:
                step_response_processed += "No response\n"
        else:
            if 'model_response_decoded' in step_response['handler_response'].keys():
                handler_responses = step_response['handler_response']['model_response_decoded']
            else:
                handler_responses = [step_response['handler_response']['content']]
            for handler_response in handler_responses:
                if handler_response is not None:
                    step_response_processed += handler_response + "\n"
                
        step_response_processed = step_response_processed[:-1]
        tool_responses = step_response['tool_response']
        if len(tool_responses) > 0:
            step_response_processed += "<br><br><b>Model Execution💻: </b><br>"
        for tool_response in tool_responses:
            if 'content' in tool_response.keys():
                content = tool_response['content']
                if content is not None:
                    step_response_processed += content + "\n"
        return step_response_processed
      
    def update_turn(self, entry_id, turn_id):
        """
        Update the turn response for a given entry and turn index
        """
        entry_1 = self.result_1.iloc[entry_id]
        entry_2 = self.result_2.iloc[entry_id]
        processed_step_response_1, processed_step_response_2 = self.get_processed_step_response(entry_id, turn_id=turn_id)
        return processed_step_response_1, processed_step_response_2