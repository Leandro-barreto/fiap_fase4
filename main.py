import argparse
from src.data.prepare_data import download_and_prepare_data
from src.models.train import train_model
from src.models.evaluate import evaluate_model
from src.inference.predict import predict_next_close

def main():
    parser = argparse.ArgumentParser(description="Pipeline LSTM para previsão de ações")
    parser.add_argument("--ticker", type=str, default="AAPL", help="Ticker da ação (ex: AAPL)")
    parser.add_argument("--start", type=str, default="2020-01-01", help="Data de início dos dados")
    parser.add_argument("--end", type=str, default="2024-12-31", help="Data de fim dos dados")
    parser.add_argument("--mode", type=str, choices=["train", "predict", "all"], default="all",
                        help="Modo de execução: train, predict ou all")
    parser.add_argument("--target_date", type=str, default="2025-01-01",
                        help="Data desejada para a previsão no formato YYYY-MM-DD (apenas para modo predict/all)")

    args = parser.parse_args()

    if args.mode in ["train", "all"]:
        print("Etapa 1: Preparando os dados...")
        download_and_prepare_data(ticker=args.ticker, start_date=args.start, end_date=args.end)

        print("Etapa 2: Treinando o modelo...")
        train_model(ticker=args.ticker)

        print("Etapa 3: Avaliando o modelo...")
        evaluate_model(ticker=args.ticker)

    if args.mode in ["predict", "all"]:
        print("Etapa 4: Fazendo inferência com dados mais recentes...")
        pred, date = predict_next_close(ticker=args.ticker, target_date=args.target_date)
        print(f"Preço previsto de fechamento para {date} - {args.ticker}: ${pred:.2f}")

if __name__ == "__main__":
    main()
