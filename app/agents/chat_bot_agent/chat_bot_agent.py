from app.agents.chat_bot_agent.tool_handler import ToolHandle
from app.agents.llm.llm import GeminiLLM 
import re

class ChatBotAgent():
    @staticmethod
    def get_response(query,path,index_name = None):

        # if (
        # (query.startswith('"') and query.endswith('"')) or
        # (query.startswith('“') and query.endswith('”')) or
        # (query.startswith("'") and query.endswith("'"))
        # ):
        #     query = query[1:-1].strip()

            
        print(f"Answering using {"LLM Knowledge" if path == None else path.capitalize() + " Search"}")
        
        data = ToolHandle.get_context(query,path,index_name)

        prompt = ""
        if path == "vector":
            prompt = query if not data else f"""You are a helpful assistant extracting answers from context for a user's query.

                        Use the provided context (retrieved via a vector search or a web search) to answer the user query and Respond in the user's expected language and translate only if needed.
                        If no context is given, use your own knowledge to answer the question clearly.

                        Follow this exact format for the response:

                        Answer: A short, direct answer to the question. Focus only on what's asked. And do not mention that you have extracted this answer from a context

                        Context:
                        - If context is provided: Copy **directly relevant** sentence(s) from the context and summarize. No extra explanation.  
                        - If no context is provided: Write “No external context was provided, so this answer is based on general knowledge.”
                       
                        Pages and Sections: Format it exactly like this, using bullet points
                        - Pages:  Only the page numbers that were used to get the answer,
                        - Sections: No extra explanation Just the sections. Use Only 1-2 sections titles that were used to get the answer. Use the given sections . But if the sections are not given , What might be the section for the given context depending on the examples in the given context (e.g."3.2 Engagement in Public Debates","Coal Industry","Industrial Revolution"," Receiving of Independence to Sri Lanka"," Impact on the Society"). 
                        
                        Context:
                        {data} 

                        User Query: {query}
                        """
        if path == None:
            prompt = f""" Answer the Users query using your genaral knowledge and past conversations 
                        Query :
                        {query}"""
        if path =="web":
            prompt = f""" You are an assistant with access to the following search results. Your task is to answer the user's query by using **the information available below**. If the answer is incomplete or missing information, **use whatever is available** to provide the most relevant response. Please answer to the best of your ability based on what you know.

                        Here are the search results:
                        {data}

                        Question: {query}"""
       
        result = GeminiLLM.get_response(prompt,query)
        return result