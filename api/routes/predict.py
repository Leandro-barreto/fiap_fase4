from fastapi import APIRouter, UploadFile, File, HTTPException
from api.schemas import PredictionRequest, PredictionResponse
from api.model.loader import load_model_ticker
from api.utils import prepare_input_for_prediction, inverse_transform_close, fetch_data
from datetime import date
import pandas as pd

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    model = load_model_ticker(request.ticker)

    print(request.data)
    if request.data:
        X_input, scaler = prepare_input_for_prediction(request.data)
        prediction_date = request.target_date or "custom_input"
    else:
        if (not request.target_date) or (request.target_date > date.today()):
            request.target_date = date.today()
        df, prediction_date = fetch_data(request.ticker, end_date=request.target_date)
        print(df.head())
        X_input, scaler = prepare_input_for_prediction(df.to_dict(orient="records"))

    y_pred = model.predict(X_input)
    y_real = inverse_transform_close(y_pred, scaler)

    return PredictionResponse(
        ticker=request.ticker,
        predicted_close=y_real[0],
        prediction_date=prediction_date
    )


@router.post("/predict/from_csv", response_model=PredictionResponse)
async def predict_from_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao ler o arquivo CSV.")

    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in df.columns for col in expected_cols):
        raise HTTPException(status_code=400, detail=f"CSV deve conter as colunas: {expected_cols}")

    ticker = file.filename.split("_")[0].upper()

    try:
        model = load_model_ticker(ticker)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Modelo para ticker '{ticker}' não encontrado.")

    X_input, scaler = prepare_input_for_prediction(df.to_dict(orient="records"))
    y_pred = model.predict(X_input)
    y_real = inverse_transform_close(y_pred, scaler)

    last_date = pd.to_datetime(df["Date"]).max() if "Date" in df.columns else pd.Timestamp.today().date()

    return PredictionResponse(
        ticker=ticker,
        predicted_close=y_real[0],
        prediction_date=last_date
    )
