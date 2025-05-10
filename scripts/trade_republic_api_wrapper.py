import asyncio
import json
import pandas as pd
import websockets


async def subscribe(uri, isin):
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

        sub_message = json.dumps({"type": "instrument", "id": isin})
        await websocket.send(f"sub 1 {sub_message}")
        print(f"Sent subscription request: {sub_message}")

        sub_response = await websocket.recv()
        print("Subscription response received.")
        return sub_response[sub_response.find("{"):]


def extract_info_from_isin(isin):
    data = json.loads(asyncio.run(subscribe("wss://api.traderepublic.com", isin)))
    info = {
        "sector": data["tags"][0]["name"],
        "name": data["exchanges"][0]["nameAtExchange"]
    }
    return info


if __name__ == "__main__":
    print(extract_info_from_isin("US8334451098"))
