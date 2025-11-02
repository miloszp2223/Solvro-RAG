import os
import json
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import re
import difflib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "../database/cocktail_dataset.json")
INDEX_DIR = os.path.join(BASE_DIR, "../cocktail_index")


# init embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Load cocktail data
def load_cocktail_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    docs = []
    for c in data:
        tags = c.get('tags') or []
        text = f"""
Name: {c.get('name')}
Category: {c.get('category')}
Glass: {c.get('glass')}
Tags: {', '.join(tags)}
Alcoholic: {'Yes' if c.get('alcoholic') else 'No'}
Ingredients: {', '.join([i.get('name') for i in c.get('ingredients', [])])}
Instructions: {c.get('instructions')}
"""
        docs.append(Document(page_content=text))
    return docs

# build / load FAISS index
def build_index():
    index_file = os.path.join(INDEX_DIR, "index.faiss")
    if os.path.exists(index_file):
        db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    else:
        docs = load_cocktail_data()
        db = FAISS.from_documents(docs, embeddings)
        os.makedirs(INDEX_DIR, exist_ok=True)
        db.save_local(INDEX_DIR)
    return db

db = build_index()

# Suggest cocktail tool
def suggest_cocktail(ingredients_str: str):
    # Convert string into a list
    ingredients = [i.strip() for i in ingredients_str.replace(" and ", ",").split(",")]

    # Create query string for similarity search
    query = ", ".join(ingredients)
    docs = db.similarity_search(query, k=3)

    if not docs:
        return "No matching cocktail found in the database."

    context_lines = []
    for d in docs:
        # Extract Name, Ingredients, and Instructions only once
        name_match = re.search(r'Name:\s*(.*)', d.page_content)
        ingredients_match = re.search(r'Ingredients:\s*(.*)', d.page_content)
        instructions_match = re.search(r'Instructions:\s*(.*)', d.page_content)

        if name_match and ingredients_match and instructions_match:
            name = name_match.group(1).strip()
            ing = ingredients_match.group(1).strip()
            instr = instructions_match.group(1).strip()
            context_lines.append(f"Name: {name}\nIngredients: {ing}\nInstructions: {instr}\n")

    return "\n".join(context_lines)

# Cocktail info tool
def cocktail_info(cocktail_name: str):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cocktail_name = cocktail_name.strip().lower()

    #DB names list
    names = [c.get("name", "").lower() for c in data]

    #fuzzy match
    match = difflib.get_close_matches(cocktail_name, names, n=1, cutoff=0.7)

    if match:
        correct_name = match[0]
        # Extract drink data
        for c in data:
            if c.get("name", "").lower() == correct_name:
                tags = c.get('tags') or []
                ingredients = ", ".join([i.get('name') for i in c.get('ingredients', [])])
                info = f"""
Name: {c.get('name')}
Category: {c.get('category')}
Glass: {c.get('glass')}
Tags: {', '.join(tags)}
Alcoholic: {'Yes' if c.get('alcoholic') else 'No'}
Ingredients: {ingredients}
Instructions: {c.get('instructions')}
"""
                return info.strip()

    return "No matching cocktail found in the database."

