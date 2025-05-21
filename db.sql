DROP TABLE IF EXISTS search_results;
CREATE TABLE IF NOT EXISTS search_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mwu TEXT NOT NULL,
    meaning TEXT NOT NULL,
    comment TEXT,
    text TEXT NOT NULL,
    translation TEXT NOT NULL,
    context TEXT NOT NULL,
    roles TEXT NOT NULL,
    expression TEXT,
    sound BOOLEAN DEFAULT 0,
    sound_path TEXT
);
INSERT INTO search_results (
        mwu,
        meaning,
        comment,
        text,
        translation,
        context,
        roles,
        expression,
        sound,
        sound_path
    )
VALUES (
        "Да ладно",
        "Удивление, недоверие",
        null,
        "— Не-не. Вот, сидим в палатке. Только-только всё разобрали, это мы купнулись. Представляешь?
    — Да ладно?
    — Заставил отец, да.",
        "— Nuh-uh. Here we are, sitting in a tent. We've just sorted everything out, and we're the ones who've been swimming. Can you imagine?
    — No way.
    — Dad’s orders.",
        "Бытовой",
        "Родители",
        "Удивление",
        1,
        "audio/1.wav"
    );