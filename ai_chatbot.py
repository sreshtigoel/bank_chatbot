import datetime
from datetime import datetime
import boto3
from langchain_aws import ChatBedrock
from langchain.memory import ConversationBufferWindowMemory
from ai_memory import memory_store_ai_assiatant
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

class ChatBot:

    def __init__(self):
        self.boto3Session = boto3.Session(profile_name="amplify")
        print("BOTO3 Session attempting")
        # config = Config(read_timeout=1500)
        self.boto3_bedrock = self.boto3Session.client("bedrock-runtime", region_name='us-east-1')
        print("boto3 successful")
        self.claudeV2_llm = ChatBedrock(
                model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
                streaming = True,
                client=self.boto3_bedrock,
                model_kwargs={"temperature": 0.3}
            )
        self.error_module = "AI ASSISTANT"
        
    def SearchAssistantAgent(self, input_text, session_id, date, description, deposit, withdraw, balance):
        try:
            memoryId = session_id
            if memoryId not in memory_store_ai_assiatant:
                memory_store_ai_assiatant[memoryId] = {
                    "memory": ConversationBufferWindowMemory(
                        output_key="output",
                        memory_key='chat_history',
                        k=10,
                        return_messages=True
                    ),
                    "last_accessed": datetime.now()
                }
            else:
                memory_store_ai_assiatant[memoryId]["last_accessed"] = datetime.now()

            memory_chat: ConversationBufferWindowMemory = memory_store_ai_assiatant[memoryId]["memory"]
            print("entring the prompt")

            system ="""
            You are Jarvis from Iron Man. You will act as an AI chatbot help assistant for Silicon Valley Bank. You have the tranaction details of the customer you are helping. Help them with any questions they may have about their own account details or any of the services that the bank provides. 

            Instructions:
            1. You have the account details of the customer which inclues date of trasaction, description of transaction, deposit amount, withdraw amount and balance amount.
            2. The description of the transaction includes infomation about the mode of transction.
            3. You need to visit the official Silicon Valley Bank website to refer to any information about the bank's services or any particular questions the user may ask about the bank.
            4. If the question asked by the user is not enough for you to help or is ambigious, you can ask the user to provide more information. 
            5. You should be able to handle gramatical and syntax errors. 
            6. Be concise in your answers. 
            """

            human = """
            date: {date}
            description: {description}
            deposit: {deposit}
            withdraw: {withdraw}
            balance: {balance}
            
            Chat History: {chat_history}
            Question: {input_text}

            """
            prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                input_variables=[],
                template=system
            ),
            HumanMessagePromptTemplate.from_template(
                input_variables=["input_text", "date", "description", "deposit", "withdraw", "balance", "chat_history"],
                template=human
            )
        ])

            full_ai_response = prompt | self.claudeV2_llm

            for response in full_ai_response.stream({"input_text": input_text, "date": date, "description": description, "deposit": deposit, "withdraw": withdraw, "balance": balance, "chat_history": memory_chat.buffer}):
                response_content = response.content
                memory_chat.save_context(inputs={"input": input_text}, outputs={"output": response_content})
                print(response_content)
                yield response_content
                    
        except Exception as e:
            print(str(e))
            yield {"Error": str(e)}
            