import streamlit as st
from auth import create_users_table, register_user, login_user

# Inicializa o banco de dados
create_users_table()

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
            st.success(f"Bem-vindo(a), {user[1]}!")
            st.write("🔜 A próxima etapa será o acesso ao banco de questões.")
        else:
            st.error("Email ou senha inválidos.")
