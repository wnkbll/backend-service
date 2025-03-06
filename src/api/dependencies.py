from typing import Annotated

from fastapi import Depends

from src.core.settings import Settings, get_app_settings

SettingsDependency = Annotated[Settings, Depends(get_app_settings, use_cache=True)]
