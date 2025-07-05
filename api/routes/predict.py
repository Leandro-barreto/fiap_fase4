from fastapi import APIRouter, UploadFile, File, HTTPException
from api.schemas import PredictionRequest, PredictionResponse
from api.model.loader import load_model_and_scaler
from api.utils import prepare_input_for_prediction, inverse_transform_close, fetch_latest_data
import pandas as pd

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    model, scaler = load_model_and_scaler(request.ticker)

    if request.data:
        X_input = prepare_input_for_prediction(request.data, scaler)
        prediction_date = request.target_date or "custom_input"
    else:
        df, prediction_date = fetch_latest_data(request.ticker)
        X_input = prepare_input_for_prediction(df.to_dict(orient="records"), scaler)

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

    # Verificar se as colunas esperadas estão presentes
    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in df.columns for col in expected_cols):
        raise HTTPException(status_code=400, detail=f"CSV deve conter as colunas: {expected_cols}")

    # Inferir o ticker do nome do arquivo (ex: AAPL_data.csv)
    ticker = file.filename.split("_")[0].upper()

    try:
        model, scaler = load_model_and_scaler(ticker)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Modelo para ticker '{ticker}' não encontrado.")

    X_input = prepare_input_for_prediction(df.to_dict(orient="records"), scaler)
    y_pred = model.predict(X_input)
    y_real = inverse_transform_close(y_pred, scaler)

    return PredictionResponse(
        ticker=ticker,
        predicted_close=y_real[0],
        prediction_date=pd.to_datetime(df.index[-1]).date() if df.index.name else pd.Timestamp.today().date()
    )
