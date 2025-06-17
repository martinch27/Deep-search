# deep_researcher/utils/id_utils.py

import uuid

def generate_session_id() -> str:
    """
    Генерирует компактный уникальный идентификатор сессии длиной 16 символов.
    Пример: '5c17f0a23e6d4f2a'
    """
    return uuid.uuid4().hex[:16]