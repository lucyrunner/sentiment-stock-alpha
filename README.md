# 📊 Sentiment–Attention Alpha

🚀 A social-sentiment–driven trading signal pipeline with Redis and backtesting.

---

## 🔍 Overview

This project implements a **single-ticker social sentiment and attention pipeline** inspired by academic research on **investor sentiment** and **investor attention**.

It combines:
- 💬 **StockTwits comments**
- 📰 **Investing.com textual content**

to construct:
- 🧠 **Sentiment indices**
- 👀 **Attention indices**

and then generates **Buy / Sell / Hold** signals with full **backtesting**.

🎯 Philosophy:  
**Start with one ticker, make it work end-to-end, then scale.**

---

## ✨ Key Features

- 📥 Social data ingestion (StockTwits + Investing.com)
- 🧠 Bull / Bear / Neutral sentiment classification
- 👀 Attention index with rolling z-score
- 🗄️ Redis-based storage and deduplication
- 📈 Buy / Sell / Hold signal generation
- 🔄 Backtesting with forward returns
- 📊 Plots for sentiment, attention, and price signals

---

## 🗂️ Project Structure

sentiment-attention-alpha/
├── src/
├── scripts/
├── tests/
├── README.md
└── pyproject.toml

---

## ⚙️ Setup

```bash
git clone https://github.com/your-username/sentiment-attention-alpha.git
cd sentiment-attention-alpha
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
redis-server
```

---

## ▶️ Run Example (OKLO)

```bash
python scripts/run_ingest.py --ticker OKLO --hours 72
python scripts/run_features.py --ticker OKLO --bucket-minutes 60 --lookback-days 90
python scripts/run_backtest.py --ticker OKLO --bucket-minutes 60 --lookback-days 90
```

---

## ⚠️ Disclaimer

This project is for research and educational purposes only.
