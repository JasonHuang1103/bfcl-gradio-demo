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
        When the entry_id is changed, update
        * num_turns
        * chatbot history
        * metrics
        """
        entry_1 = self.result_1.iloc[entry_id]
        entry_2 = self.result_2.iloc[entry_id]
        num_turn_1, num_turn_2 = entry_1['num_turns'], entry_2['num_turns']
        self.max_num_turn = min(num_turn_1, num_turn_2) - 1
        processed_step_response_1, processed_step_response_2 = self.get_processed_step_response(entry_id, turn_id=0)
        return num_turn_1, num_turn_2, processed_step_response_1, processed_step_response_2
      
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
        if 'model_response_decoded' in step_response['handler_response'].keys():
            handler_responses = step_response['handler_response']['model_response_decoded']
        else:
            handler_responses = [step_response['handler_response']['content']]
        for handler_response in handler_responses:
            step_response_processed += handler_response + "\n"
        step_response_processed = step_response_processed[:-1]
        tool_responses = step_response['tool_response']
        if len(tool_responses) > 0:
            step_response_processed += "<br><br><b>Model Execution💻: </b><br>"
        for tool_response in tool_responses:
            if 'content' in tool_response.keys():
                step_response_processed += tool_response['content'] + "\n"
        return step_response_processed
      
    def update_turn(self, entry_id, turn_id):
        """
        Update the turn response for a given entry and turn index
        """
        entry_1 = self.result_1.iloc[entry_id]
        entry_2 = self.result_2.iloc[entry_id]
        processed_step_response_1, processed_step_response_2 = self.get_processed_step_response(entry_id, turn_id=turn_id)
        return processed_step_response_1, processed_step_response_2
        