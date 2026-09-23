def serialize_search_result(row):
    """
    Сериализует строку из БД в словарь
    
    Args:
        row: sqlite3.Row объект
    
    Returns:
        Словарь с данными записи
    """
    return {
        "id": row["id"],
        "mwu": row["mwu"],
        "meaning": row["meaning"],
        "comment": row["comment"],
        "text": row["text"],
        "translation": row["translation"],
        "context": row["context"],
        "roles": row["roles"],
        "sound": bool(row["sound"]),
        "sound_path": row["sound_path"],
    }

