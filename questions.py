import sqlite3


def create_questions_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            theme TEXT NOT NULL,
            level TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL
        )
    '''
    )

    c.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            selected_option TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def insert_sample_questions():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    questions = [
        (
            "Frações",
            "Ensino Fundamental",
            "Qual é o resultado de 1/2 + 1/3?",
            "5/6",
            "2/5",
            "3/4",
            "1/6",
            "a"
        ),
        (
            "Porcentagem",
            "Ensino Médio",
            "Um produto que custava R$200 teve um desconto de 25%. Qual é o novo preço?",
            "R$150",
            "R$175",
            "R$180",
            "R$160",
            "a"
        ),
        (
            "Equações",
            "Ensino Médio",
            "Qual o valor de x na equação 2x - 4 = 10?",
            "x = 6",
            "x = 7",
            "x = 5",
            "x = 4",
            "a"
        )
    ]

    c.executemany('''
        INSERT INTO questions (theme, level, question, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', questions
                  )


    conn.commit()
    conn.close()
