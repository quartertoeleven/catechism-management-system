from typing import Any, Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    custom_data: Optional[dict[str, Any]] = None