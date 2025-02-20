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
        self.update_model(model_name_1, model_name_2)

    def update_model(self, model_name_1, model_name_2):
        """
        Takes in the models names and updates the state
        """
        model_1_path = f'./judge_result/20250128_124000/{model_name_1}_error_analysis.csv'
        model_2_path = f'./judge_result/20250128_124000/{model_name_2}.csv'
        self.model_name_1 = model_name_1
        self.model_name_2 = model_name_2
        self.result_1 = get_result(model_1_path)
        self.result_2 = get_result(model_2_path)
      
    def update_entry(self, entry_id):
        """
        When the entry_id is changed, return error information for both models
        """
        entry_1 = self.result_1[self.result_1['entry_id'] == entry_id].iloc[0]
        entry_2 = self.result_2[self.result_2['entry_id'] == entry_id].iloc[0]
        
        error_info_1 = {
            'type': entry_1['error_reason_type'],
            'description': entry_1['error_reason_description'],
            'turn_id': entry_1['error_turn_id']
        }
        error_info_2 = {
            'type': entry_2['error_reason_type'],
            'description': entry_2['error_reason_description'],
            'turn_id': entry_2['error_turn_id']
        }
        
        return error_info_1, error_info_2
      