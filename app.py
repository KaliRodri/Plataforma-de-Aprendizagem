import streamlit as st
from auth import create_users_table, register_user, login_user
from questions import get_random_question, create_questions_table, insert_sample_questions
from ai_assistant import explain_error
import sqlite3

create_users_table()
create_questions_table()
# insert_sample_questions()


st.set_page_config(page_title="Plataforma", page_icon="📚")
st.title("📚 Plataforma de Aprendizagem com IA")

menu = st.sidebar.selectbox("Menu", ["Login", "Registrar"])

if menu == "Registrar":
    st.subheader("Criar nova conta")
    name = st.text_input("Nome completo")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Registrar"):
        if name and email and password:
            success = register_user(name, email, password)
            if success:
                st.success("Conta criada com sucesso! Faça login.")
            else:
                st.error("Esse email já está registrado.")
        else:
            st.warning("Preencha todos os campos.")

elif menu == "Login":
    st.subheader("Acessar sua conta")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_user = user
            st.success(f"Bem-vindo(a), {user[1]}!")
            st.write("🔜 A próxima etapa será o acesso ao banco de questões.")
        else:
            st.error("Email ou senha inválidos.")

if "logged_user" in st.session_state:
    user = st.session_state.logged_user
    email = user[2]  
    name = user[1]  
    st.subheader("📝 Responda à questão abaixo:")

  
    if "question_data" not in st.session_state:
        st.session_state.question_data = get_random_question()

    question_data = st.session_state.question_data

    if question_data:
        q_id, theme, level, question, a, b, c, d, correct = question_data

        st.write(f"**Tema:** {theme}  |  **Nível:** {level}")
        st.write(question)

        options = {
            f"A) {a}": "a",
            f"B) {b}": "b",
            f"C) {c}": "c",
            f"D) {d}": "d"
        }

        selected_label = st.radio("Escolha uma opção:", list(options.keys()))
        selected = options[selected_label]

        if st.button("Enviar Resposta"):
            is_correct = 1 if selected == correct else 0

            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO attempts (user_email, question_id, selected_option, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (email, q_id, selected, is_correct))
            conn.commit()
            conn.close()

            if is_correct:
                st.success("✅ Resposta correta!")
            else:
                st.error("❌ Resposta incorreta.")
                name = user[1]  # Pega o nome do usuário logado
                explicacao = explain_error(
                name,
                question,
                {"a": a, "b": b, "c": c, "d": d},
                correct,
                selected,
                theme
            )
                st.info("💡 Explicação:")
                st.write(explicacao)

            # Libera para sortear nova questão na próxima vez
            del st.session_state.question_data
