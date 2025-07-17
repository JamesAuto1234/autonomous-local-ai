import time
from loguru import logger
from local_ai.model import MODELS
from local_ai.config import DEFAULT_MODEL_DIR
from huggingface_hub import hf_hub_download

def download_model_from_hf(model_name: str, attempt: int = 3) -> str:
    
    repo_id = MODELS[model_name]["repo"]
    file_name = MODELS[model_name]["file"]
    file_path = DEFAULT_MODEL_DIR / file_name
    
    if file_path.exists():
        return True, file_path
    
    for _ in range(attempt):
        try:
            hf_hub_download(
                repo_id = repo_id,
                filename = file_name,
                local_dir = DEFAULT_MODEL_DIR
            )
            logger.success(f"Model {model_name} downloaded successfully")
            
            return True, DEFAULT_MODEL_DIR / file_name
        except Exception as e:
            logger.warning(f"Failed to download model {model_name} after {_ + 1} attempts")
            time.sleep(1)
    logger.error(f"Failed to download model {model_name} after {attempt} attempts")
    return False, None
