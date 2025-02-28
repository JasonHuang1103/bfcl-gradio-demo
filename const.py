import os

RESULT_PATH = './result_score/2025-02-09/result/'

DEFAULT_MODEL_1 = 'claude-3-5-sonnet-20241022-FC'
DEFAULT_MODEL_2 = 'DeepSeek-V3-FC'

MODELS = sorted([f for f in os.listdir(RESULT_PATH) if os.path.isdir(os.path.join(RESULT_PATH, f))])

for model in MODELS:
    print(model)