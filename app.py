from flask import Flask, render_template, request, jsonify
import torch
import ollama
from openai import OpenAI
import os
import json
import PyPDF2
import re
import pyttsx3
from flask_featureflags import FeatureFlag

app = Flask(__name__)

# Initialize FeatureFlag
feature_flags = FeatureFlag(app)

# Configuration for feature flags
app.config['FEATURE_FLAGS'] = {
    'voice_enabled': True  # Set this to True to enable voice by default
}

# Initialize Ollama models
ollama.pull('llama2')
ollama.pull('mxbai-embed-large')

# Initialize OpenAI client for Ollama
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3'
)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load vault content and generate embeddings
def load_vault():
    vault_content = []
    if os.path.exists("vault.txt"):
        with open("vault.txt", "r", encoding='utf-8') as vault_file:
            vault_content = vault_file.readlines()
    
    vault_embeddings = []
    for content in vault_content:
        response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
        vault_embeddings.append(response["embedding"])
    
    return torch.tensor(vault_embeddings), vault_content

vault_embeddings_tensor, vault_content = load_vault()

# Function to get relevant context
def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:
        return []
    
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

# Function to rewrite query
def rewrite_query(user_input, conversation_history, ollama_model):
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])
    prompt = f"""Rewrite the following query by incorporating relevant context from the conversation history.
    The rewritten query should:
    - Preserve the core intent and meaning of the original query
    - Expand and clarify the query to make it more specific and informative for retrieving relevant context
    - Avoid introducing new topics or queries that deviate from the original query
    - DONT EVER ANSWER the Original query, but instead focus on rephrasing and expanding it into a new query
    Return ONLY the rewritten query text, without any additional formatting or explanations.

    Conversation History:
    {context}

    Original query: [{user_input}]

    Rewritten query:
    """

    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )
    
    rewritten_query = response.choices[0].message.content.strip()
    return rewritten_query

# Function for Ollama chat
def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    conversation_history.append({"role": "user", "content": user_input})
    
    if len(conversation_history) > 1:
        rewritten_query = rewrite_query(user_input, conversation_history, ollama_model)
    else:
        rewritten_query = user_input
    
    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content)
    context_str = "\n".join(relevant_context) if relevant_context else ""
    
    user_input_with_context = user_input + "\n\nRelevant Context:\n" + context_str if relevant_context else user_input
    conversation_history[-1]["content"] = user_input_with_context
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content, rewritten_query, context_str

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Flask routes
@app.route('/')
def index():
    voice_enabled = app.config['FEATURE_FLAGS']['voice_enabled']
    return render_template('index.html', voice_enabled=voice_enabled)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text. Also bring in extra relevant information to the user query from outside the given context."
    conversation_history = request.json.get('conversation_history', [])
    
    response, rewritten_query, context = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, 'llama2', conversation_history)
    
    # Convert the response to speech if voice is enabled
    if app.config['FEATURE_FLAGS']['voice_enabled']:
        text_to_speech(response)
    
    return jsonify({
        'response': response,
        'rewritten_query': rewritten_query,
        'context': context
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = file.filename
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension == '.pdf':
            text = convert_pdf_to_text(file)
        elif file_extension == '.txt':
            text = file.read().decode('utf-8')
        elif file_extension == '.json':
            data = json.load(file)
            text = json.dumps(data, ensure_ascii=False)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        append_to_vault(text)
        global vault_embeddings_tensor, vault_content
        vault_embeddings_tensor, vault_content = load_vault()
        
        return jsonify({'message': 'File uploaded and processed successfully'})

@app.route('/toggle_voice', methods=['POST'])
def toggle_voice():
    current_state = app.config['FEATURE_FLAGS']['voice_enabled']
    app.config['FEATURE_FLAGS']['voice_enabled'] = not current_state
    return jsonify({'voice_enabled': not current_state})

def convert_pdf_to_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + " "
    return text

def append_to_vault(text):
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < 1000:
            current_chunk += (sentence + " ").strip()
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk)
    
    with open("vault.txt", "a", encoding="utf-8") as vault_file:
        for chunk in chunks:
            vault_file.write(chunk.strip() + "\n")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)