# app/utils/nfc.py
from typing import Dict, Optional


def validate_nfc_tag(tag_id: str, expected_id: Optional[str] = None) -> Dict:
    """
    Validate NFC tag information
    This is a stub - in a real application, this would interface with NFC hardware or API
    """
    if expected_id and tag_id != expected_id:
        return {
            "valid": False,
            "message": "Invalid NFC tag ID"
        }
    
    return {
        "valid": True,
        "tag_id": tag_id,
        "message": "Valid NFC tag"
    }
