import pandas as pd



def analyze_csv(file):

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()
    required_columns = [
    "equipment name",
    "type",
    "flowrate",
    "pressure",
    "temperature"
]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    total_equipment = len(df)

    avg_flowrate = round(df["flowrate"].mean(), 2)
    avg_pressure = round(df["pressure"].mean(), 2)
    avg_temperature = round(df["temperature"].mean(), 2)

    type_counts = df["type"].value_counts()

    type_distribution = {
        "raw": {k: int(v) for k, v in type_counts.items()},
        "chart": {
            "labels": [str(x) for x in type_counts.index],
            "values": [int(v) for v in type_counts.values]
        }
    }

    summary = {
    "total_equipment": int(len(df)),
    "averages": {
        "flowrate": float(df["flowrate"].mean()),
        "pressure": float(df["pressure"].mean()),
        "temperature": float(df["temperature"].mean())
    },
    "type_distribution": type_distribution
}


    return summary, df.to_dict(orient="records")



