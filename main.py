from fastapi import FastAPI
from pydantic import BaseModel
from twilio.rest import Client
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

class CallRequest(BaseModel):
    to: str
    message: str

@app.post("/call")
async def make_call(request: CallRequest):
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    call = client.calls.create(
        to=request.to,
        from_=os.getenv("TWILIO_NUMBER"),
        twiml=f"<Response><Say voice='alice' language='pt-BR'>{request.message}</Say></Response>"
    )
    return {"status": "ligando", "sid": call.sid}

# Servir o HTML diretamente na raiz
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/valicaller_render.html")

# Tornar a pasta 'static' acessível
app.mount("/static", StaticFiles(directory="static"), name="static")
