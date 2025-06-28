import google.generativeai as genai

genai.configure(api_key="#")


def explain_error(nome_aluno, pergunta, alternativas, alternativa_correta, alternativa_escolhida, tema):
    prompt = f"""
    O estudante {nome_aluno} errou a seguinte questão de {tema}:
    
    Pergunta: {pergunta}
    Alternativas:
A) {alternativas['a']}
B) {alternativas['b']}
C) {alternativas['c']}
D) {alternativas['d']}

    Resposta escolhida: {alternativas[alternativa_escolhida]} ({alternativa_escolhida.upper()})
Resposta correta: {alternativas[alternativa_correta]} ({alternativa_correta.upper()})

Explique diretamente ao aluno, pelo nome, de forma clara e didática:
- Onde provavelmente ele errou
- Qual o raciocínio correto
- Como ele pode aprender esse conteúdo
- Use tom motivador e respeitoso, como um bom professor faria.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
