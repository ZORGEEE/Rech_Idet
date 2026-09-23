from database.connection import get_db_connection
from database.repositories.expression_repository import ExpressionRepository


class FilterService:
    """Сервис для работы с фильтрами"""
    
    def __init__(self):
        self.expression_repo = ExpressionRepository()
    
    def get_filter_options(self):
        """
        Получить все доступные значения для фильтров
        
        Returns:
            Словарь с ключами фильтров и списками значений
        """
        conn = get_db_connection()
        filters = {}
        
        # Получаем уникальные значения для каждого поля (кроме sound)
        for field in ['mwu', 'context', 'roles']:
            rows = conn.execute(
                f"SELECT DISTINCT {field} FROM search_results WHERE {field} IS NOT NULL AND {field} != '' ORDER BY {field} ASC"
            ).fetchall()
            filters[field] = [row[field] for row in rows]
        
        # Получаем выражения
        filters['expression'] = self.expression_repo.get_all_distinct()
        
        # Добавляем опции для звука
        filters['sound'] = ["Есть звук", "Нет звука"]
        
        conn.close()
        return filters

