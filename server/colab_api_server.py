"""Custom vewSnake API server for Google Colab (FastAPI + SDXL-Turbo + ngrok).

How to use (Google Colab, T4 GPU runtime):
1. Open a new notebook at https://colab.research.google.com
2. Runtime -> Change runtime type -> T4 GPU
3. Copy this file's contents into a cell and run it
4. Copy the printed ngrok URL, then run locally:
       vewsnake -p "your prompt" --api https://xxxx.ngrok-free.app/generate

Requires: pip install fastapi uvicorn diffusers transformers torch accelerate nest-asyncio pyngrok pillow
"""

import io

import nest_asyncio
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pyngrok import ngrok
from diffusers import StableDiffusionPipeline

app = FastAPI(title="vewSnake Custom API Server", version="1.0")

print("AI model is loading, please wait...")
model_id = "stabilityai/sdxl-turbo"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")
print("Model successfully loaded into GPU memory!")


@app.post("/generate")
def generate_image(payload: dict) -> StreamingResponse:
    prompt = payload.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt logic missing.")
    try:
        image = pipe(prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return StreamingResponse(img_byte_arr, media_type="image/png")
    except Exception as exc:  # noqa: BLE001 - server boundary handler
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# Optional: set your free ngrok authtoken from https://dashboard.ngrok.com
# ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN")

public_url = ngrok.connect(8000)
print("\nYour custom vewSnake API is live!")
print(f"API Endpoint URL: {public_url.public_url}/generate\n")

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
