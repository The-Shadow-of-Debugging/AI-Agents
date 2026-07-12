import os
import arxiv
from uuid import uuid4
import time

from typing import List, Any, Literal, TypedDict, Annotated
from pydantic import BaseModel, Field
import operator
import re

from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
# from langchain.chains.summarize import load_summarize_chain
from langgraph.graph import StateGraph, END

MODEL_NAME = 'qwen2.5:3b'
MODEL = OllamaLLM(model=MODEL_NAME)


class Subtopic(BaseModel):
    title: str = Field(..., description='Technical title of research subtopic')
    description: str = Field(..., description='1-2 sentence explanation')


class SubtopicList(BaseModel):
    subtopics: List[Subtopic]


class ResearchPaper(BaseModel):
    title: str = Field(default="Untitled Paper", description='Title of research paper')
    authors: str = Field(default="Unknown Authors", description='Comma-separated author names')
    abstract: str = Field(default="", description='Abstract content')
    url: str = Field(default="#", description='ArXiv URL')
    published: str = Field(default="Unknown Date", description="Publication date")


class ResearchResult(BaseModel):
    subtopic: Subtopic
    papers: List[ResearchPaper]
    research_gap: str


class State(TypedDict):
    topic: str
    subtopics: List[Subtopic]
    approval: Literal['pending', 'approved', 'rejected']
    research_results: Annotated[List[ResearchResult], operator.add]


def fetch_arxiv_papers(query: str, max_results: int = 3) -> List[ResearchPaper]:
    """Fetch papers from arXiv"""
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []
        for result in client.results(search):
            authors = ", ".join(author.name for author in result.authors)  # Исправлена опечатка

            # ИСПРАВЛЕНО: используем result.summary вместо result.abstract
            papers.append(ResearchPaper(
                title=result.title,
                authors=authors,
                abstract=result.summary,  # Вот здесь исправление
                url=result.entry_id,
                published=str(result.published.date()) if result.published else "Unknown Date",
            ))

        return papers  # Исправлен отступ - должен быть вне цикла for

    except Exception as e:
        print(f"Error fetching arXiv papers for '{query}': {str(e)}")
        return []


def generate_subtopics(state: State) -> State:
    """Generate research subtopics for the given topic"""
    try:
        parser = PydanticOutputParser(pydantic_object=SubtopicList)
        prompt = PromptTemplate(
            template=(
                '''You are a senior AI researcher specializing in LLM architectures.\n
                Given topic: {topic}\n
                Provide exactly 3 narrow, technical subtopics.\n
                Output JSON Object: {{ "subtopics": [ {{ "title":"...", "description":"..." }}, ... ] }}\n
                {format_instructions}
                '''
            ),
            input_variables=["topic"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | MODEL | parser
        out: SubtopicList = chain.invoke({"topic": state["topic"]})
        return {"subtopics": out.subtopics, "approval": "pending"}
    except Exception as e:
        print(f"Subtopic generation error: {str(e)}")
        return {"subtopics": [
            Subtopic(title="Technical Subtopic 1", description="Fallback description"),
            Subtopic(title="Technical Subtopic 2", description="Fallback description"),
            Subtopic(title="Technical Subtopic 3", description="Fallback description")
        ], "approval": "pending"}


def ask_approval(state: State) -> State:
    """Ask user for approval of generated subtopics"""
    try:
        print("\n" + "=" * 50)
        print("Generated research subtopics:")
        print("=" * 50)

        for i, st in enumerate(state["subtopics"], 1):
            print(f'\n{i}. {st.title}')
            print(f'   Description: {st.description}')

        ans = input("\nDo you accept these subtopics? (yes/no/edit)\n> ").lower().strip()

        if ans.startswith('y'):
            return {"approval": "approved"}  # Исправлена опечатка: "approved"
        elif ans.startswith('e'):
            print("\nEnter revised topics (one per line, empty line to finish):")
            new_topics = []
            for i in range(3):
                title = input(f"\nTitle {i + 1}: ").strip()
                if not title:
                    break
                desc = input(f"Description {i + 1}: ").strip()
                if title and desc:
                    new_topics.append(Subtopic(title=title, description=desc))
            return {"subtopics": new_topics, "approval": "approved"}  # Исправлена опечатка
        else:
            return {"approval": "rejected"}
    except Exception as e:
        print(f"Approval error: {str(e)}")
        return {"approval": "approved"}  # Исправлена опечатка


def analyze_papers(papers: List[ResearchPaper], subtopic: str) -> str:
    """Analyze papers and identify research gaps"""
    try:
        if not papers or papers[0].title == "Error: Paper not found":
            return "No papers available for analysis"

        paper_info = "\n\n".join([
            f"Paper {i + 1}: {p.title}\n"
            f"URL: {p.url}\n"
            f"Abstract: {p.abstract[:500]}...\n"
            f"Published: {p.published}\n"
            for i, p in enumerate(papers)
        ])

        gap_prompt = PromptTemplate(
            input_variables=["subtopic", "papers_info"],
            template=(
                "Analyze these three research papers on {subtopic}:\n\n"
                "{papers_info}\n\n"
                "Identify ONE specific research gap considering:\n"
                "- What limitations do these papers share?\n"
                "- What opportunities do they collectively miss?\n"
                "- What technical challenges remain unaddressed?\n"
                "Provide a concise gap description based on all three papers.\n"
                "Include references to specific papers where appropriate.\n"
                "Format: [concise_description]"
            )
        )

        gap = (gap_prompt | MODEL).invoke({
            "subtopic": subtopic,
            "papers_info": paper_info
        })

        gap = re.sub(r'^(Gap:?\s*)+', '', gap, flags=re.IGNORECASE).strip()
        return gap if gap else "No specific research gap identified"
    except Exception as e:
        print(f"Gap analysis error: {str(e)}")
        return "Research gap analysis failed"


def conduct_research(state: State) -> State:
    """Conduct research for each subtopic"""
    try:
        if state.get("approval") != "approved":
            print("Research not approved, skipping...")
            return {"research_results": []}

        research_results = []

        for subtopic in state["subtopics"]:
            print(f"\n{'=' * 50}")
            print(f"Researching: {subtopic.title}")
            print(f"{'=' * 50}")

            papers = fetch_arxiv_papers(subtopic.title, max_results=3)
            print(f"Found {len(papers)} papers for '{subtopic.title}'")

            gap = analyze_papers(papers, subtopic.title)

            research_results.append(ResearchResult(
                subtopic=subtopic,
                papers=papers,
                research_gap=gap,
            ))

        return {"research_results": research_results}
    except Exception as e:
        print(f"Critical research error: {str(e)}")
        return {"research_results": []}


def compile_report(state: State) -> State:
    """Compile research results into a report"""
    try:
        if not state.get("research_results"):
            return {"report": "# Research Report\n\nNo results generated"}

        report = f"# Research Report: {state['topic']}\n\n"
        report += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        for result in state["research_results"]:
            report += f"## {result.subtopic.title}\n"
            report += f"*{result.subtopic.description}*\n\n"

            report += '### Key Papers\n'
            for i, paper in enumerate(result.papers, 1):
                report += f"#### Paper {i}: {paper.title}\n"
                report += f"- **URL**: {paper.url}\n"
                report += f"- **Authors**: {paper.authors}\n"
                report += f"- **Published**: {paper.published}\n"
                report += f"- **Abstract**: {paper.abstract[:300]}...\n\n"

            report += "### Identified Research Gap\n"
            report += f"{result.research_gap}\n\n"
            report += "---\n\n"

        filename = f"research_report_{state['topic'].replace(' ', '_').lower()}_{int(time.time())}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\nResearch report saved as {filename}")
        return {"report": report}
    except Exception as e:
        print(f"Report compilation error: {str(e)}")
        return {"report": f"# Error: report generation failed\n\n{str(e)}"}


# Build the state graph
builder = StateGraph(State)

builder.add_node("generate_subtopics", generate_subtopics)
builder.add_node("get_approval", ask_approval)
builder.add_node("conduct_research", conduct_research)
builder.add_node("compile_report", compile_report)

builder.set_entry_point("generate_subtopics")
builder.add_edge("generate_subtopics", "get_approval")


def route_approval(state: State) -> str:
    """Route based on approval status"""
    if state.get("approval") == "approved":  # Исправлена опечатка
        return "conduct_research"
    elif state.get("approval") == "rejected":
        return "END"
    else:
        return "generate_subtopics"


builder.add_conditional_edges(
    'get_approval',
    route_approval,
    {
        'conduct_research': 'conduct_research',
        'generate_subtopics': 'generate_subtopics',
        'END': END
    }
)

builder.add_edge('conduct_research', 'compile_report')
builder.add_edge('compile_report', END)

research_agent = builder.compile()

# Save the graph visualization
try:
    graph = research_agent.get_graph(xray=True)
    png_bytes = graph.draw_mermaid_png()
    with open("research_agent_graph.png", "wb") as f:
        f.write(png_bytes)
    print("Graph visualization saved as research_agent_graph.png")
except Exception as e:
    print(f"Could not save graph visualization: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Academic Research Agent System")
    print("=" * 50)

    topic = input("\nEnter your research topic: ").strip()

    if not topic:
        topic = "Large Language Models"
        print(f"Using default topic: {topic}")

    init_state = State(
        topic=topic,
        subtopics=[],
        approval="pending",
        research_results=[]
    )

    start_time = time.time()

    try:
        final_state = research_agent.invoke(init_state)

        print("\n" + "=" * 50)
        print(f"Research completed for: {topic}")
        print("=" * 50)

        if final_state.get("research_results"):
            print(f"\nGenerated {len(final_state['research_results'])} research areas:")
            for i, result in enumerate(final_state["research_results"], 1):
                print(f"\n{i}. {result.subtopic.title}")
                print(f"   Gap: {result.research_gap[:100]}...")
        else:
            print("No research results were generated.")

    except Exception as e:
        print(f"\nError during research execution: {str(e)}")

    duration = time.time() - start_time
    print(f"\nTotal Execution Time: {duration:.2f} seconds")