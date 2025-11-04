import os
from llama_cpp import Llama


from tools.rag_tool import suggest_cocktail, cocktail_info

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "./LLM/Llama-3.2-1B-Instruct-Q4_K_M.gguf")


def LLM_info_test(cocktail_name: str):
    result = cocktail_info(cocktail_name)
    prompt = f"""
    You are a cocktail expert.
    Tell something about the cocktail:
    {cocktail_name}
    based on the following information
    {result}
    
    """
    response = llm(prompt, max_tokens=150)
    return response['choices'][0]['text'].strip()


def LLM_suggestion_test(ingredients: str = "", tags: str = "") -> str:
    if (tags == ""):
        input = ingredients
    elif(ingredients == ""):
        input = tags
    else:
        input = ingredients + ", " + tags
    result = suggest_cocktail(input)
    #print(result)

    prompt = f"""You are a cocktail expert.
Here are some cocktails you know about:
{result}

Task:
Pick the ONE cocktail from the list above that best matches these ingredients: {ingredients}.

Rules:
- Only use cocktails from the list.
- Do not invent or modify cocktails.
- Give a short reason for your choice.
"""

    prompt = prompt.strip()

    response = llm(prompt, max_tokens=100)
    # extract text
    text = response['choices'][0]['text'].strip()

    return text

llm = Llama(model_path=MODEL_PATH, n_ctx=1024, n_threads=os.cpu_count(), temperature=0.4)
if __name__ == "__main__":
    print("\n-----Nowy prompt----\n")
    print(LLM_suggestion_test("gin, tonic"))
    print("\n-----Nowy prompt----\n")
    print(LLM_suggestion_test("rum, coke", "sweet"))
    print("\n-----Nowy prompt----\n")
    print(LLM_suggestion_test("rum", "citrusy, alcoholic"))
    print("\n-----Nowy prompt----\n")
    print(LLM_info_test("Mojito"))
