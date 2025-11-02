from fastmcp import FastMCP
import sys
print("PYTHON EXECUTABLE USED BY LM STUDIO:", sys.executable)
from tools.rag_tool import suggest_cocktail, cocktail_info

mcp = FastMCP(name="Cocktail RAG Server")

@mcp.tool
def cocktail_suggestion(ingredients: str) -> str:
    return suggest_cocktail(ingredients)

@mcp.tool
def cocktail_details(name: str) -> str:
    return cocktail_info(name)

if __name__ == "__main__":
    mcp.run()
