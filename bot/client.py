import logging
from typing import Dict, Optional
import aiohttp
from config.settings import Config

logger = logging.getLogger(__name__)


class APIClient:
    """Клиент для работы с API"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or Config.API_BASE_URL
    
    def _build_url(self, path: str) -> str:
        """Построить полный URL"""
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
    
    async def fetch_json(self, path: str, params: Optional[Dict[str, str]] = None) -> Dict:
        """
        Выполнить GET запрос к API
        
        Args:
            path: путь к endpoint
            params: параметры запроса
        
        Returns:
            JSON ответ от API
        
        Raises:
            RuntimeError: если запрос завершился с ошибкой
        """
        url = self._build_url(path)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    text = await response.text()
                    raise RuntimeError(f"API error {response.status}: {text}")
                return await response.json()
    
    async def get_filter_options(self) -> Dict:
        """Получить доступные фильтры"""
        return await self.fetch_json("filter-options")
    
    async def search_results(self, filters: Dict[str, str]) -> Dict:
        """Выполнить поиск"""
        return await self.fetch_json("search-results", params=filters)
    
    async def get_result_by_id(self, result_id: int) -> Dict:
        """Получить результат по ID"""
        return await self.fetch_json(f"search-results/{result_id}")

