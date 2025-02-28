from huanzhi_utils import load_file, write_list_of_dicts_to_file
import pandas as pd

def standardize_step_response(input_step_response):
    step_response = {}
    step_response["assistant_response"] = input_step_response[0]
    step_response["handler_response"]  = input_step_response[1]
    step_response["tool_response"] = input_step_response[2:]
    step_response["num_tools"] = len(
        step_response["handler_response"].get("model_response_decoded", [])
    )
    return step_response

def standardize_turn_response(result):
    input_turn_response, end_of_turn_state = result    
    turn_response = {}
    turn_response["end_of_turn_state"] = end_of_turn_state
    turn_response["turn_eval_message"] = input_turn_response["begin_of_turn_query"]
    keys = list(input_turn_response.keys())
    keys.remove("begin_of_turn_query")
    keys = sorted(keys, key=lambda x: int(x.split("_")[-1]))
    step_responses = []
    for idx, key in enumerate(keys):
        assert key.endswith(f"_{idx}")
        step_responses.append(input_turn_response[key])
    
    turn_response["step_responses"] = [standardize_step_response(step_response) for step_response in step_responses]
    turn_response["num_steps"] = len(step_responses) - 1
    return turn_response

def standardize_inference_response(result):
    inference_response = {}
    inference_response["id"] = result["id"]
    inference_response["result"] = result["result"]
    
    # Handle optional fields
    inference_response["inference_log"] = result.get("inference_log", [])  # Default to empty list if missing
    inference_response["input_token_count"] = result.get("input_token_count", [])
    inference_response["output_token_count"] = result.get("output_token_count", [])
    inference_response["latency"] = result.get("latency", [])
    
    return inference_response
  
def get_result(result_path):
    result_list = load_file(result_path)
    result_standardized = [standardize_inference_response(result) for result in result_list]
    return pd.DataFrame(result_standardized)