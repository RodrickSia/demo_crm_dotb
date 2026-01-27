from typing import Any, List

def extract_response_data(response: Any) -> List[Any]:
    if hasattr(response, "data"):
        return response.data
    elif isinstance(response, dict):
        return response.get("data", [])
    return []
