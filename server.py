from fastmcp import FastMCP
import sys
print("PYTHON EXECUTABLE USED BY LM STUDIO:", sys.executable)
from tools.rag_tool import suggest_cocktail, cocktail_info

mcp = FastMCP(name="Cocktail RAG Server")

@mcp.tool(
    name="cocktail_suggestion",
    description="Returns matching cocktails. Takes ingredients and optional tags (like sweet, bitter, etc.) as arguments",
)
def cocktail_suggestion(ingredients: str = "", tags: str = "") -> str:
    if tags == "":
        keywords = ingredients
    elif ingredients == "":
        keywords = tags
    else:
        keywords = ingredients + ", " + tags
    return suggest_cocktail(keywords)

@mcp.tool(
    name="cocktail_details",
    description="Returns information on specific cocktail. Takes cocktail names as arguments",
)
def cocktail_details(name: str) -> str:
    return cocktail_info(name)

if __name__ == "__main__":
    mcp.run()
