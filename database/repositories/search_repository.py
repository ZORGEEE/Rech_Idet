from database.connection import get_db_connection


class SearchRepository:
    """Репозиторий для работы с таблицей search_results"""
    
    @staticmethod
    def get_by_id(result_id: int):
        """Получить запись по ID"""
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM search_results WHERE id = ?", (result_id,)
        ).fetchone()
        conn.close()
        return row
    
    @staticmethod
    def search(filters: dict):
        """
        Поиск записей с фильтрами
        
        Args:
            filters: словарь с фильтрами (mwu, context, roles, sound)
        
        Returns:
            Список найденных записей
        """
        query_parts = [
            "SELECT sr.*, GROUP_CONCAT(e.expression, '||') AS expressions_concat",
            "FROM search_results sr",
            "LEFT JOIN expressions e ON sr.id = e.search_result_id",
            "WHERE 1 = 1",
        ]
        params = []
        
        if filters.get("mwu"):
            query_parts.append("AND sr.mwu = ?")
            params.append(filters["mwu"])
        if filters.get("context"):
            query_parts.append("AND sr.context = ?")
            params.append(filters["context"])
        if filters.get("roles"):
            query_parts.append("AND sr.roles = ?")
            params.append(filters["roles"])
        if filters.get("expression"):
            query_parts.append("AND e.expression = ?")
            params.append(filters["expression"])
        if filters.get("sound") == "Есть звук":
            query_parts.append("AND sr.sound = 1")
        elif filters.get("sound") == "Нет звука":
            query_parts.append("AND sr.sound = 0")
        
        query_parts.append("GROUP BY sr.id ORDER BY sr.id ASC")
        sql = " ".join(query_parts)
        
        conn = get_db_connection()
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        
        return rows
    
    @staticmethod
    def search_form(filters: dict):
        """
        Поиск для веб-формы (без GROUP_CONCAT)
        
        Args:
            filters: словарь с фильтрами
        
        Returns:
            Список найденных записей
        """
        query = '''
            SELECT sr.*
            FROM search_results sr
            LEFT JOIN expressions e ON sr.id = e.search_result_id
        '''
        
        wheres = ['1 = 1']
        params = []
        
        if filters.get('mwu'):
            wheres.append('sr.mwu = ?')
            params.append(filters['mwu'])
        if filters.get('context'):
            wheres.append('sr.context = ?')
            params.append(filters['context'])
        if filters.get('roles'):
            wheres.append('sr.roles = ?')
            params.append(filters['roles'])
        if filters.get('expression'):
            wheres.append('e.expression = ?')
            params.append(filters['expression'])
        if filters.get('sound') == "Есть звук":
            wheres.append('sr.sound = 1')
        elif filters.get('sound') == "Нет звука":
            wheres.append('sr.sound = 0')
        
        query += ' WHERE ' + ' AND '.join(wheres)
        query += ' GROUP BY sr.id'
        
        conn = get_db_connection()
        results = conn.execute(query, params).fetchall()
        conn.close()
        
        return results

