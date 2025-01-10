from typing import Dict, List, Optional, Union
from fastapi import BackgroundTasks, FastAPI, Request, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
from pydantic import BaseModel
import ai_chatbot
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
event_stream_media_type = "text/event-stream"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

class RequestModelAIAssistant(BaseModel):
    inputText: str
    sessionId: str
    statementFile: str

@app.post("/ai-chatbot/help-assistant")
async def run_text_sql_job_ai_assistant(request_model: RequestModelAIAssistant):
    error_message = "Something went wrong. Please check the conditions and try again."
    media_type = event_stream_media_type
    
    try:
        input_text = request_model.inputText
        session_id = request_model.sessionId
        statement_file = request_model.statementFile

        if not statement_file:
            raise HTTPException(status_code=400, detail="Statement file is missing.")

        # Read the CSV file
        try:
            # file_content = await statement_file.read_()
            # df = pd.read_csv(pd.compat.StringIO(file_content.decode('utf-8')))
            print("before reading the file")
            df = pd.read_csv(statement_file)
            print("after reading the file")
        except Exception as e:
            print("in exception block")
            raise HTTPException(status_code=400, detail=f"Failed to read the statement file: {str(e)}")

        # Ensure the required columns exist
        # required_columns = {"date", "description", "deposit", "withdraw", "balance"}
        # missing_columns = required_columns - set(df.columns)
        # if missing_columns:
        #     raise HTTPException(status_code=400, detail=f"Missing columns in statement file: {', '.join(missing_columns)}")

        # Extract column data
        print("reading data into cols")
        date = df["Date"].tolist()
        description = df["Description"].tolist()
        deposit = df["Deposits"].tolist()
        withdraw = df["Withdrawls"].tolist()
        balance = df["Balance"].tolist() 
        print("done reading data into cols")       

        chatbot = ai_chatbot.ChatBot()

        response =  chatbot.SearchAssistantAgent(input_text, session_id, date, description, deposit, withdraw, balance)

        return StreamingResponse(response, media_type="text/event-stream")
        
        
    except Exception as e:
        # obj = eh.errorHandlerClass()
        # obj.handle_error(e, 0, "AI ASSISTANT")
        print(e)
        return StreamingResponse(e, media_type=media_type)