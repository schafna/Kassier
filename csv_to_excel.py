import pandas as pd
from pathlib import Path
                
def csv_to_excel(path_to_csv_file: str, output_file_name: str = "filterd_csv_to_xls") -> pd.DataFrame:
    output_file_name = output_file_name + ".xlsx"

    new_line = "Buchungsdatum;Informationen;Valutadatum;Betrag;Waehrung;Daten_mit_Uhrzeit\n"

    if path_to_csv_file[0] == "\"" and path_to_csv_file[-1] == "\"":
        path_to_csv_file = path_to_csv_file[1:-1]
    if path_to_csv_file[0] == "\"":
        path_to_csv_file = path_to_csv_file[1:]
    if path_to_csv_file[-1] == "\"":
        path_to_csv_file = path_to_csv_file[0:-1]

    with open(path_to_csv_file, "r") as original_file:
        original_content = original_file.read()

    with open("new_file.csv", "w") as new_file:
        new_file.write(new_line + original_content)

    csv_file = Path("new_file.csv")
    df = pd.read_csv(csv_file, delimiter=";")

    df["Informationen"] = df["Informationen"].astype(str)


    series = pd.Series(df["Informationen"])

    for index in range(len(series)):
        if series[index].split()[0] == "Online":
            # Find the starting and ending positions of the desired information
            start_pos = series[index].find("Empfänger:") + len("Empfänger:")
            end_pos = series[index].rfind("IBAN")

            # Extract the desired information using string slicing
            series[index] = series[index][start_pos:end_pos].strip()

        if series[index].split()[0] == "Auftraggeber:":
            start_pos = series[index].find("Auftraggeber:") + len("Auftraggeber:")
            end_pos = series[index].rfind("IBAN")
            series[index] = series[index][start_pos:end_pos].strip()

        if series[index].split()[0] == "Verwendungszweck:":
            zusatz = "Kartenzahlung bei: "
            start_pos = series[index].find("Verwendungszweck:") + len("Verwendungszweck:")
            end_pos = series[index].rfind("Zahlungsreferenz:")
            series[index] = zusatz + series[index][start_pos:end_pos].strip()


    df["Informationen"] = series

    df = df[["Buchungsdatum", "Informationen", "Betrag"]]

    betrag_series = pd.Series(df["Betrag"])

    positive = []
    negative = []
    for value in betrag_series:
        value = value.replace(".", "")
        value = float(value.replace(",", "."))
        if value < 0:
            positive.append(None)
            value = abs(value)
            value = str(value)
            value = value.replace(".", ",")
            negative.append(value)
        else:
            value = abs(value)
            value = str(value)
            value = value.replace(".", ",")
            positive.append(value)
            negative.append(None)

    df["Einnahmen"] = positive
    df["Ausgaben"] = negative
    df["Beleg_Nr"] = [None]* len(positive)
    df["Kategorie"] = [None]* len(positive)
    df["Einnahmen1"] = [None]* len(positive)
    df["Ausgaben1"]= [None]* len(positive)

    df = df[["Buchungsdatum", "Beleg_Nr","Kategorie","Informationen", "Einnahmen1", "Ausgaben1", "Einnahmen", "Ausgaben"]]
    
    #df.to_excel(output_file_name, index=False)
    return df
