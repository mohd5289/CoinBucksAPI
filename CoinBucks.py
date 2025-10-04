#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 09:35:08 2025

@author: Osuolale
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uuid
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(filename="transactions.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Dummy exchange rates (crypto → Naira)
EXCHANGE_RATES = {
    "BTC": 25000000,
    "ETH": 1500000,
    "USDT": 1000
}

class TransactionRequest(BaseModel):
    amount_in_crypto: float
    crypto_type: str
    recipient_bank: str

class TransactionResponse(BaseModel):
    transaction_id: str
    crypto_type: str
    recipient_bank: str
    conversion_rate: float
    final_amount_naira: float

@app.post("/transactions", response_model=TransactionResponse)
async def create_transaction(request: Request, txn: TransactionRequest):
    # Validate crypto type
    if txn.crypto_type not in EXCHANGE_RATES:
        raise HTTPException(status_code=400, detail="Unsupported crypto type")

    conversion_rate = EXCHANGE_RATES[txn.crypto_type]
    final_amount = txn.amount_in_crypto * conversion_rate
    transaction_id = str(uuid.uuid4())

    response_data = TransactionResponse(
        transaction_id=transaction_id,
        crypto_type=txn.crypto_type,
        recipient_bank=txn.recipient_bank,
        conversion_rate=conversion_rate,
        final_amount_naira=final_amount
    )

    # Log request & response
    logging.info(f"Request: {txn.dict()} | Response: {response_data.dict()}")

    return response_data



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("CoinBucks:app", host="127.0.0.1", port=8000, reload=True)



