import pandas as pd
from mistral.mistral_api import get_mistral_response

def convert_df_to_json_for_sector(df, sector, percentage_sold_total, percentage_bought_total):
    df = df[df["Sector"] == sector]
    print(df)
    companies = []

    for i in df.index:
        company_dict = {
            "title": df.at[i, "Name"],
            "percentage_sold": float(df.at[i, "SellPct"]) / percentage_sold_total,
            "percentage_bought": float(df.at[i, "BuyPct"]) /percentage_bought_total,
            "amount_bought": float(df.at[i, "BuyTotal"]),
            "amount_sold": float(df.at[i, "SellTotal"])
        }
        companies.append(company_dict)
    return companies


def convert_df_to_json(df):
    category_counts = df["Sector"].value_counts()
    threshold = 2
    df["Sector"] = df["Sector"].apply(lambda x: x if category_counts[x] >= threshold else "Other")

    sector_df = df.groupby("Sector").sum().reset_index().drop("Name", axis=1)
    sectors = []

    for i in sector_df.index:
        sector = sector_df.at[i, "Sector"]
        percentage_sold_total = round(sector_df.at[i, "SellPct"], 4)
        percentage_bought_total = round(sector_df.at[i, "BuyPct"], 4)
        sector_dict = {
            "title": sector,
            "percentage_sold": percentage_sold_total,
            "percentage_bought":  percentage_bought_total,
            "amount_bought":  round(sector_df.at[i, "BuyTotal"],4),
            "amount_sold": round(sector_df.at[i, "SellTotal"],4),
            "Elements": convert_df_to_json_for_sector(df, sector, percentage_sold_total, percentage_bought_total)
        }
        sectors.append(sector_dict)
    prompt = f"can you please write one short short sentence about the data here in a funny way about the most popular sector {sectors}"
    message = get_mistral_response(prompt)
    return {"sectors" : sectors, "message" : message}


if __name__ == "__main__":
    df = pd.DataFrame({
        "Sector": ["Tech", "Finance", "Tech", "Finance", "Consumer Goods"],
        "Name": ["Company A", "Company B", "Company C", "Company D", "Company E"],
        "BuyPct": [20, 20, 20, 10, 30],
        "SellPct": [28.5, 40.2, 30.9, 55.3, 45.7],
        "BuyTotal": [150000, 220000, 100000, 300000, 180000],
        "SellTotal": [120000, 195000, 130000, 270000, 200000]
    })

    print(convert_df_to_json(df))
