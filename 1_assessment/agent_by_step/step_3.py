from typing import List, Any, Dict
from pydantic import BaseModel, Field

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from langgraph.graph import StateGraph, START, END

MODEL_NAME = 'qwen2.5:3b'
MODEL = OllamaLLM(model=MODEL_NAME)

class Subtopic(BaseModel):
    title: str = Field(...)
    description: str = Field(...)

class SubtopicList(BaseModel):
    subtopics: List[Subtopic]

parser = PydanticOutputParser(pydantic_object=SubtopicList)

def generate_subtopics(state: Dict[str, Any]) -> Dict[str, Any]:
    prompt = PromptTemplate(
        template=(
            '''
            {format_instructions}\n
            You are a senior AI researcher specializing in LLM architectures.\n
            Given topic: {topic}\n
            Provide exactly 3 narrow, technical subtopics.\n
            Output JSON Object: {{ \"subtopics\": [ {{ \"title\":\"...\", \"description\":\"...\" }}, ... ] }}\n
            '''
        ),
        input_variables=["topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | MODEL | parser
    out: SubtopicList = chain.invoke({"topic": state["topic"]})
    return {"subtopics": out.subtopics}

def ask_approval(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\nGenerateed subtopics:")
    for(i, st) in enumerate(state["subtopics"], 1):
        print(f'{i+1}: {st.title} - {st.description}')
    ans = input("\nDo you accept accept these? (yes/no)\n> ")
    return {"approval": ans.strip().lower()}

class State(Dict[str, Any]):
    topic: str
    subtopics: List[Subtopic]
    approval: str

builder = StateGraph(State)
builder.add_node("generate", generate_subtopics)
builder.add_node("approval_node", ask_approval)

builder.add_edge(START, "generate")
builder.add_edge("generate", "approval_node")

def route(state: Dict[str, Any]) -> str:
    return END if state.get("approval", "").startswith('y') else 'generate'

builder.add_conditional_edges(
    'approval_node',
    route,
    {'generate': 'generate', END: END }
)

graph = builder.compile()

graph_png = graph.get_graph(xray=True)
png_bytes = graph_png.draw_mermaid_png()
with open("simple_agent.png", "wb") as f:
    f.write(png_bytes)

if __name__ == "__main__":
    final_state = graph.invoke({"topic": "Emotional alignment research"})
    print("\nFinal approved subtopics:")
    for st in final_state["subtopics"]:
        print(f"- {st.title}: {st.description}")
