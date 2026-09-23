from database.repositories.search_repository import SearchRepository
from database.repositories.expression_repository import ExpressionRepository
from utils.serializers import serialize_search_result


class SearchService:
    """Сервис для работы с поиском"""
    
    def __init__(self):
        self.search_repo = SearchRepository()
        self.expression_repo = ExpressionRepository()
    
    def get_result_by_id(self, result_id: int):
        """
        Получить результат поиска по ID с выражениями
        
        Args:
            result_id: ID записи
        
        Returns:
            Словарь с данными записи и выражениями, или None если не найдено
        """
        row = self.search_repo.get_by_id(result_id)
        if not row:
            return None
        
        expressions = self.expression_repo.get_by_search_result_id(result_id)
        result = serialize_search_result(row)
        result["expressions"] = expressions
        return result
    
    def search(self, filters: dict):
        """
        Поиск записей с фильтрами
        
        Args:
            filters: словарь с фильтрами
        
        Returns:
            Список словарей с результатами поиска
        """
        rows = self.search_repo.search(filters)
        
        payload = []
        for row in rows:
            item = serialize_search_result(row)
            if row.get("expressions_concat"):
                item["expressions"] = row["expressions_concat"].split("||")
            else:
                item["expressions"] = []
            payload.append(item)
        
        return payload
    
    def search_form(self, filters: dict):
        """
        Поиск для веб-формы
        
        Args:
            filters: словарь с фильтрами
        
        Returns:
            Список sqlite3.Row объектов
        """
        return self.search_repo.search_form(filters)

