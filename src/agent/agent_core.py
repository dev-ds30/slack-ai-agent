import os
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI

class SentientAgent:
    def __init__(self, openai_api_key=None):
        key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=key, temperature=0.2)
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are an ambient assistant.\n"
                "Context:\n{context}\n\n"
                "Based on the above, suggest an actionable step for:\n{question}"
            )
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def suggest(self, context, question):
        return self.chain.run({"context": context, "question": question})
