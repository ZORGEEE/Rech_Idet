DROP TABLE IF EXISTS search_results;
CREATE TABLE search_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mwu TEXT NOT NULL,
    meaning TEXT NOT NULL,
    comment TEXT,
    text TEXT NOT NULL,
    translation TEXT NOT NULL,
    context TEXT NOT NULL,
    roles TEXT NOT NULL,
    sound BOOLEAN DEFAULT 0,
    sound_path TEXT
);
DROP TABLE IF EXISTS expressions;
CREATE TABLE expressions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_result_id INTEGER NOT NULL,
    expression TEXT NOT NULL,
    FOREIGN KEY (search_result_id) REFERENCES search_results(id) ON DELETE CASCADE
);
INSERT INTO search_results (
        mwu,
        meaning,
        comment,
        text,
        translation,
        context,
        roles,
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
    — Dad's orders.",
        "Бытовой",
        "Родители",
        -- "Удивление",
        1,
        "audio/1.wav"
    ),
    (
        "Как раз",
        " = 'Это именно то, что оправдано' (используется, чтобы усилить утверждение)",
        null,
        "— Просто бывает написано, ну как будто бы. У тебя никогда такого не было? Каждое слово понятно, но вместе в предложение их встроить — и получится просто ад какой-то.<br>— Это <strong>как раз</strong> очень чётко оправдано. Просто умом мы ещё не дошли до того уровня, до которого дошёл этот человек.",
        "— You know how sometimes it's written,
        like...sort of.You never had this happen ? Every word makes sense,
        but
        when you try to fit them into a sentence — it just turns into complete gibberish.< br > — That 's actually very justified. It' s just that our minds haven 't reached the level this person has reached yet.",
        "Учебный",
        "Знакомые",
        -- "Усиление, Злость",
        0,
        "audio/0.wav"
    );
INSERT INTO expressions (search_result_id, expression)
VALUES (1, "Удивление"),
    (2, "Усиление"),
    (2, "Злость");