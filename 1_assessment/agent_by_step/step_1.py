from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

MODEL_NAME = 'qwen2.5:3b'
llm = OllamaLLM(model=MODEL_NAME)

prompt_template = PromptTemplate(
    template=(
        '''
        You are a senior AI researcher specializing in LLM architectures.\n
        Given topic: {topic}\n
        Provide exactly 3 narrow, technical subtopics.\n
        '''
    ),
    input_variables=["topic"],
)

chain = prompt_template | llm
response = chain.invoke({'topic': 'Emotional alignment'})
print(response)