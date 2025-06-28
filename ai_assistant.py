import google.generativeai as genai

genai.configure(api_key="AIzaSyBNJresJSERYhCs6qJTEdoLm_b-hVJBJLQ")

def explain_error(pergunta, alternativa_errada, tema):
    prompt = f"""
    Um estudante errou a seguinte questão de {tema}:
    
    Pergunta: {pergunta}
    Resposta escolhida: {alternativa_errada}
    
    Explique o erro e ensine de forma clara e didática como resolver esse tipo de questão, identificando pela resposta onde o estudante pode ter errado
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
