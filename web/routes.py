from flask import Blueprint, render_template, request
from services.search_service import SearchService
from services.filter_service import FilterService

web_bp = Blueprint('web', __name__)


@web_bp.route("/")
def home():
    """Главная страница"""
    return render_template("main.html")


@web_bp.route("/instruction")
def instruction():
    """Страница инструкции"""
    return render_template("instruction.html")


@web_bp.route("/for_tutors")
def for_tutors():
    """Страница для преподавателей"""
    return render_template("for_tutors.html")


@web_bp.route("/find")
def find():
    """Страница поиска"""
    service = FilterService()
    filter_options = service.get_filter_options()
    return render_template("find.html", filter_options=filter_options)


@web_bp.route("/search_result", methods=['GET', 'POST'])
def search_result():
    """Страница результатов поиска"""
    service = FilterService()
    search_service = SearchService()
    filter_options = service.get_filter_options()
    results = []
    
    if request.method == 'POST':
        # Получаем данные формы
        filters = {
            'mwu': request.form.get('mwu', ''),
            'context': request.form.get('context', ''),
            'roles': request.form.get('roles', ''),
            'expression': request.form.get('expression', ''),
            'sound': request.form.get('sound', ''),
        }
        
        # Удаляем пустые значения
        filters = {k: v for k, v in filters.items() if v}
        
        # Выполняем поиск
        results = search_service.search_form(filters)
        
        return render_template(
            "search_result.html",
            results=results,
            request=request,
            filter_options=filter_options,
            results_count=len(results)
        )
    
    return render_template(
        "search_result.html",
        results=[],
        request=request,
        filter_options=filter_options,
        results_count=0
    )


@web_bp.route("/contacts")
def contacts():
    """Страница контактов"""
    return render_template("contacts.html")


@web_bp.route("/dictionary")
def dictionary():
    """Страница словаря"""
    return render_template("dictionary.html")

