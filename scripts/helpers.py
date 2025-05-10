import pandas as pd
from mistral.mistral_api import get_mistral_response

def convert_df_to_json_for_sector(df, sector, percentage, action):
    df = df[df["Sector"] == sector]
    indices = df.sort_values(by=f'{action}Pct', ascending=False).head(5).index
    companies = []
    for i in indices:
        company_dict = {
            "name": df.at[i, "Name"],
            "percentage": f"{int(float(df.at[i, action + 'Pct']) / percentage*100)}%" if int(float(df.at[i, action + 'Pct']) / percentage*100)>1 else "<1%",
        }
        companies.append(company_dict)
    return companies


def convert_df_to_json(df):
    sold = convert_type_df_to_json(df, action="Sell")
    bought = convert_type_df_to_json(df, action="Buy")
    return {"sold" : sold,
            "bought" : bought}

def convert_type_df_to_json(df, action="Buy"):
    sector_df = df.groupby("Sector").sum().reset_index().drop("Name", axis=1)
    indices = sector_df.sort_values(by=f'{action}Pct', ascending=False).head(5).index
    sectors = []
    for i in indices:
        sector = sector_df.at[i, "Sector"]
        percentage = round(sector_df.at[i, f"{action}Pct"], 4)
        sector_dict = {
            "name":  sector,
            "percentage": f"{int(percentage*100)}%" if int(percentage*100)>1 else "<1%" ,
            "subcategories": convert_df_to_json_for_sector(df, sector, percentage, action)
        }
        sectors.append(sector_dict)
    return sectors



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
