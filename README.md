# Solvro-RAG

Narzędzie służy do sugerowania koktajli na podstawie składników oraz podawania informacji o nich, korzystające z modelu LLM.  

Projekt był tworzony i testowany w środowisku Pycharm.


## Instalacja

Przed użyciem narzędzia zainstaluj wszystkie zależności w wirtualnym środowisku:

   pip install -r requirements.txt

## Testowanie narzędzia w LMstudio przez MCP

1. Pobierz model LLM kompatybilny z MCP w LMstudio  
   (testowane na: _Llama 3.2 1B Instruct GGUF Q4_K_M_ oraz _Meta Llama 3.1 8B Instruct GGUF Q4_K_M_)  

2. Skonfiguruj MCP w LMstudio:  
Show settings (Ctrl+B) → Program → Install → mcp.json  
Wklej konfigurację:

{
  "mcpServers": {
    "suggestion-server": {
      "command": "ścieżka do pythona w venv (.venv/Scripts/python.exe)", 
      "args": ["ścieżka do server.py"]
    }
  }
}

3. Skonfiguruj system prompt:  
Show settings (Ctrl+B) → Context → System prompt  
Wklej:
When asked about cocktails, answer only based on responses from tools.

4. Zapisz preset i ustaw go jako aktywny.  
Teraz, kiedy w czacie LMstudio użytkownik zapyta o koktajle, model LLM wywoła narzędzie MCP i zwróci odpowiedź na podstawie danych funkcji.


## Testowanie narzędzia w Pythonie
1. Pobierz kompatybilny model LLM, którego chcesz użyć do testów. Utwórz w projekcie folder LLM i umieść w nim pobrany model

2. W pliku test.py zmień nazwę modelu
      _Llama-3.2-1B-Instruct-Q4_K_M.gguf_
Na nazwę pobranego modelu

3. Możesz testować funkcje ręcznie, wywołując je w pliku Python (test.py) po linijce:

   if __name__ == "__main__":

Dostępne funkcje:  

- suggest_cocktail("składniki po przecinku") – zwraca sugestie koktajli na podstawie podanych składników  
- cocktail_info("nazwa drinka") – zwraca informacje o konkretnym koktajlu  


## Przykładowe użycie

**_W Pythonie:_**

from tools.suggest_cocktail import suggest_cocktail

from tools.cocktail_info import cocktail_info

print(suggest_cocktail("vodka, lime, sugar"))

print(cocktail_info("Margarita"))

**_W LMstudio:_**

Tell me what I can make using rum and egg whites

Tell me the recipe for Apricot Lady




## Struktura projektu
- server.py - serwer MCP
- test.py - plik służący wyłącznie do testów RAGa poprzez kompilator

- w folderze tools znajdują się narzędzia 
suggest_cocktail 
oraz
cocktail_info
- w folderze database znajduje się baza danych json z koktajlami
- w folderze cocktail znajdują się wygenerowane pliki index

## Wymagania

- Python 3.10+
- Zależności z requirements.txt
- Model LLM kompatybilny z MCP (Llama 3.x Instruct GGUF Q4_K_M)
