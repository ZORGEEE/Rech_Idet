from database.connection import get_db_connection


class ExpressionRepository:
    """Репозиторий для работы с таблицей expressions"""
    
    @staticmethod
    def get_by_search_result_id(search_result_id: int):
        """Получить все выражения для конкретного search_result"""
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT expression FROM expressions WHERE search_result_id = ? ORDER BY expression ASC",
            (search_result_id,),
        ).fetchall()
        conn.close()
        return [row["expression"] for row in rows]
    
    @staticmethod
    def get_all_distinct():
        """Получить все уникальные выражения"""
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT DISTINCT expression FROM expressions WHERE expression IS NOT NULL AND expression != '' ORDER BY expression ASC"
        ).fetchall()
        conn.close()
        return [row["expression"] for row in rows]

