from typing import Any, List

def extract_response_data(response: Any) -> List[Any]:
    if hasattr(response, "data"):
        return response.data
    elif isinstance(response, dict):
        return response.get("data", [])
    return []

def readMDFiles(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError 
    except Exception as e:
        raise e