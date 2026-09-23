import logging
from typing import Dict, Tuple
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from bot.client import APIClient

logger = logging.getLogger(__name__)


def parse_search_args(text: str) -> Tuple[Dict[str, str], list[str]]:
    """
    Парсинг аргументов поиска из текста
    
    Args:
        text: текст с параметрами вида "ключ=значение ключ2=значение2"
    
    Returns:
        Кортеж (словарь параметров, список ошибок)
    """
    allowed_keys = {"mwu", "context", "roles", "expression", "sound"}
    params: Dict[str, str] = {}
    errors: list[str] = []

    for chunk in text.split():
        if "=" not in chunk:
            errors.append(f"Игнорирую '{chunk}' — ожидаю формат ключ=значение")
            continue
        key, value = chunk.split("=", 1)
        key = key.strip().lower()
        value = value.strip()
        if key not in allowed_keys:
            errors.append(f"Неизвестный фильтр '{key}'")
            continue
        if not value:
            errors.append(f"Пустое значение для фильтра '{key}'")
            continue
        if key == "sound":
            lowered = value.lower()
            if lowered in {"yes", "есть", "sound", "1", "true"}:
                value = "Есть звук"
            elif lowered in {"no", "нет", "0", "false"}:
                value = "Нет звука"
            else:
                errors.append(
                    "Значение sound должно быть yes/нет (или 1/0, true/false)"
                )
                continue
        params[key] = value

    return params, errors


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Привет! Я помогу найти данные через API.\n"
        "Доступные команды:\n"
        "• /filters — показать доступные значения фильтров\n"
        "• /search ключ=значение ... — искать (пример: /search mwu=дом sound=yes)\n"
        "• /result <id> — подробности по ID"
    )


async def filters_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /filters"""
    client = APIClient()
    try:
        data = await client.get_filter_options()
    except Exception as exc:
        logger.exception("Failed to fetch filter options")
        await update.message.reply_text(f"Не удалось получить фильтры: {exc}")
        return

    parts = []
    for key, values in data.items():
        head = key.upper()
        if not values:
            parts.append(f"{head}: (нет вариантов)")
        else:
            sample = ", ".join(values[:10])
            suffix = "" if len(values) <= 10 else ", ..."
            parts.append(f"{head}: {sample}{suffix}")

    await update.message.reply_text("\n".join(parts))


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /search"""
    args = context.args
    if not args:
        await update.message.reply_text(
            "Использование: /search mwu=... context=... sound=yes|no"
        )
        return

    params, errors = parse_search_args(" ".join(args))
    if errors:
        await update.message.reply_text("\n".join(errors))
        return

    client = APIClient()
    try:
        data = await client.search_results(params)
    except Exception as exc:
        logger.exception("Search request failed")
        await update.message.reply_text(f"Ошибка доступа к API: {exc}")
        return

    results = data.get("results", [])
    if not results:
        await update.message.reply_text("Ничего не найдено")
        return

    lines = [f"Найдено: {data.get('count', len(results))}"]
    for item in results[:5]:
        mwu = item.get("mwu") or "—"
        meaning = item.get("meaning") or ""
        context_value = item.get("context") or ""
        lines.append(
            f"#{item.get('id')} • {mwu}\n"
            f"  Значение: {meaning}\n"
            f"  Контекст: {context_value}"
        )

    if len(results) > 5:
        lines.append("Показаны первые 5 результатов")

    await update.message.reply_text("\n".join(lines))


async def result_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /result"""
    if not context.args:
        await update.message.reply_text("Использование: /result <id>")
        return

    try:
        result_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID должен быть числом")
        return

    client = APIClient()
    try:
        data = await client.get_result_by_id(result_id)
    except Exception as exc:
        logger.exception("Failed to fetch result")
        await update.message.reply_text(f"Ошибка запроса: {exc}")
        return

    lines = [
        f"#{data.get('id')} — {data.get('mwu')}",
        f"Значение: {data.get('meaning')}",
        f"Комментарий: {data.get('comment')}",
        f"Текст: {data.get('text')}",
        f"Контекст: {data.get('context')}",
        f"Роли: {data.get('roles')}",
        f"Перевод: {data.get('translation')}",
    ]
    expressions = data.get("expressions") or []
    if expressions:
        lines.append("Выражения:")
        lines.extend(f"• {expr}" for expr in expressions)
    if data.get("sound") and data.get("sound_path"):
        lines.append(f"Звук: доступен ({data['sound_path']})")
    else:
        lines.append("Звук: нет")

    await update.message.reply_text("\n".join(lines))


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик неизвестных сообщений"""
    await update.message.reply_text(
        "Не понимаю сообщение. Используйте /search, /filters или /result."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error("Update %s caused error %s", update, context.error)


def setup_handlers(application: Application) -> None:
    """Настройка обработчиков для бота"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("filters", filters_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("result", result_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))
    application.add_error_handler(error_handler)

