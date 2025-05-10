import asyncio
import json
import pandas as pd
import time
import websockets


async def subscribe(uri, id, type="instrument", timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connecting to server...")

                await websocket.send("connect 30")
                print("Sent: connect 30")

                while True:
                    response = await websocket.recv()
                    print("Received:", response)

                    if "connected" in response:
                        print("Connection confirmed! Proceeding...")
                        break

                sub_message = json.dumps({"type": type, "id": id})
                await websocket.send(f"sub 1 {sub_message}")
                print(f"Sent subscription request: {sub_message}")

                sub_response = await websocket.recv()
                print("Subscription response received.")
                return sub_response[sub_response.find("{"):]
        except Exception:
            pass
    raise Exception("Connection timed out.")


def extract_info_from_isin(isin):
    data = json.loads(asyncio.run(subscribe("wss://api.traderepublic.com", isin)))
    exchange_id = data["exchanges"][0]["slug"]
    id = f"{isin}.{exchange_id}"
    price_info = json.loads(asyncio.run(subscribe("wss://api.traderepublic.com", id, type="ticker")))

    try:
        sector = data["tags"][0]["name"]
    except Exception:
        sector = None
    info = {
        "ISIN": isin,
        "sector": sector,
        "name": data["name"],
        "price_per_share": price_info["bid"]["price"],
        "currency": "EUR"
    }
    return info


if __name__ == "__main__":
    extract_info_from_isin("US67066G1040")
