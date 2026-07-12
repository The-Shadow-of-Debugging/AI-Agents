from pydantic import BaseModel, Field
from typing import List
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

MODEL_NAME = 'qwen2.5:3b'
llm = OllamaLLM(model=MODEL_NAME)

class Subtopic(BaseModel):
    title: str = Field(...,description='Technical title of research subtopic')
    description: str = Field(...,description='1-2 sentence explanation')

class SubtopicList(BaseModel):
    subtopics: List[Subtopic]

parser = PydanticOutputParser(pydantic_object=SubtopicList)

prompt_template = PromptTemplate(
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

chain = prompt_template | llm | parser
out: SubtopicList = chain.invoke({"topic": "Emotional alignment"})
for(i, st) in enumerate(out.subtopics):
    print(f'{i+1}: {st.title} - {st.description}')
