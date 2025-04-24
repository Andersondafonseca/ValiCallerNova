from fastapi import FastAPI
from pydantic import BaseModel
from twilio.rest import Client
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Model da requisição
class CallRequest(BaseModel):
    to: str
    message: str

# Endpoint da chamada
@app.post("/call")
async def make_call(request: CallRequest):
    try:
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        call = client.calls.create(
            to=request.to,
            from_=os.getenv("TWILIO_NUMBER"),
            twiml=f"<Response><Say voice='alice' language='pt-BR'>{request.message}</Say></Response>"
        )
        return {"status": "ligando", "sid": call.sid}
    except Exception as e:
        return {"error": str(e)}

# Serve a página HTML
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/valicaller_render.html")

# Serve arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
