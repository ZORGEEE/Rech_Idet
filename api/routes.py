from flask import Blueprint, jsonify, request
from services.search_service import SearchService
from services.filter_service import FilterService

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route("/filter-options", methods=["GET"])
def api_filter_options():
    """API endpoint для получения доступных фильтров"""
    service = FilterService()
    return jsonify(service.get_filter_options())


@api_bp.route("/search-results/<int:result_id>", methods=["GET"])
def api_get_result(result_id):
    """API endpoint для получения результата по ID"""
    service = SearchService()
    result = service.get_result_by_id(result_id)
    
    if not result:
        return jsonify({"error": "not_found"}), 404
    
    return jsonify(result)


@api_bp.route("/search-results", methods=["GET"])
def api_search_results():
    """API endpoint для поиска результатов"""
    filters = {
        "mwu": request.args.get("mwu"),
        "context": request.args.get("context"),
        "roles": request.args.get("roles"),
        "expression": request.args.get("expression"),
        "sound": request.args.get("sound"),
    }
    
    # Удаляем None значения
    filters = {k: v for k, v in filters.items() if v}
    
    service = SearchService()
    payload = service.search(filters)
    
    return jsonify({
        "count": len(payload),
        "filters": filters,
        "results": payload
    })

