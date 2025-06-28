import streamlit as st
from auth import create_users_table, register_user, login_user
from questions import get_random_question, create_questions_table, insert_sample_questions
from ai_assistant import explain_error
import sqlite3

# Inicializa o banco de dados
create_users_table()
create_questions_table()
# insert_sample_questions()

# Página principal
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
    st.subheader("📝 Responda à questão abaixo:")

    question_data = get_random_question()
    if question_data:
        q_id, theme, level, question, a, b, c, d, correct = question_data
        
        st.write(f"**Tema:** {theme}  |  **Nível:** {level}")
        st.write(question)
        
        options = {
        "a": a,
        "b": b,
        "c": c,
        "d": d
        }
        
        selected = st.radio("Escolha uma opção:" , options)
        
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
                explicacao = explain_error(question, options[selected], theme)
                st.info("💡 Explicação:")
                st.write(explicacao)
    
    
     