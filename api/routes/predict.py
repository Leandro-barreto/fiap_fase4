from fastapi import APIRouter
from api.schemas import PredictionRequest, PredictionResponse
from api.model.loader import load_model_and_scaler
from api.utils import prepare_input_for_prediction, inverse_transform_close, fetch_latest_data

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
