# 💵 Dollar Death Watch

**A live tracker of de-dollarisation signals across global reserve composition, central bank gold purchases, BRICS trade settlement, and dollar strength indices.**

Built by [Anuja A. Gokhale](https://ssrn.com/author=10973290) (MA Applied Economics, NUS Merit Scholar) as a companion to research on the Dominant Currency Paradigm.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dollar-death-watch.streamlit.app)

---

## 🔍 The Honest Verdict

De-dollarisation is real but slow. The USD reserve share has fallen from 71% in 2000 to 57% today — a structural decline over a quarter century. But 92% of recent quarterly moves are exchange-rate valuation effects, not active portfolio reallocation. Central banks are not running from the dollar. They are diversifying at the margins while keeping dollar assets as their core.

**The dollar is not dying. It is being diluted.**

---

## 📊 What the Dashboard Tracks

| Signal | Source | Latest |
|--------|--------|--------|
| USD share of global reserves | IMF COFER | 56.8% (2025Q4) |
| Central bank gold purchases | World Gold Council | 1,045t (2024) |
| BRICS non-USD trade settlement | BIS / policy announcements | ~52% est. (2025) |
| DXY annual average | FRED | 98.1 (2025) |

---

## 🔗 Why This Matters: The DCP Connection

The dollar's role as the dominant **invoice currency** in global trade is separate from — and arguably more durable than — its role as a reserve currency.

My working paper ([ssrn.com/abstract=6514338](https://ssrn.com/abstract=6514338)) documents that dollar-invoiced energy and manufactured goods costs transmit inflation from India to Singapore to the UK regardless of bilateral exchange rate movements. This is the Dominant Currency Paradigm in action: **the dollar runs global goods markets even when central banks are diversifying away from dollar reserves**.

De-dollarisation of reserves is real. De-dollarisation of trade invoicing is much slower. Understanding both layers is essential for any assessment of the dollar's future role.

---

## 🚀 Run Locally

```bash
git clone https://github.com/anujagokhale1604/dollar-death-watch
cd dollar-death-watch
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Data Sources

- **IMF COFER** — Currency Composition of Official Foreign Exchange Reserves (quarterly, 2000-2025)
- **World Gold Council** — Central bank gold demand (annual)
- **BIS / SWIFT** — Trade settlement currency estimates
- **FRED** — DXY Broad Dollar Index (DTWEXBGS)

Note: BRICS non-USD settlement estimates are approximate and based on publicly available policy announcements and BIS data. They are not official figures.

---

## 📖 Citation

```
Gokhale, A.A. (2026). Dollar Death Watch [Dashboard].
GitHub. https://github.com/anujagokhale1604/dollar-death-watch

Gokhale, A.A. (2026). Cross-Country Macroeconomic Dynamics: Inflation,
Growth, and Monetary Policy — India, Singapore, and the United Kingdom.
SSRN Working Paper. https://ssrn.com/abstract=6514338
```

---

## 📬 Contact

Anuja A. Gokhale · anujagokhale1604@gmail.com · [ssrn.com/author=10973290](https://ssrn.com/author=10973290)

---

*Built for research and educational purposes. Data updated manually from public sources.*
