import pandas as pd
                
def csv_to_excel(uploaded_file) -> pd.DataFrame:
    
    df = pd.read_csv(uploaded_file, delimiter=";")
    column_names = ["Buchungsdatum","Informationen","Valutadatum","Betrag","Waehrung","Daten_mit_Uhrzeit"]
    df.columns = column_names

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
