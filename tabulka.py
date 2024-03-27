import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

def filtruj(jmeno):
    new = df[df['Athlete'] == jmeno]
    pocty = []
    for i in range(len(new)):
        z = new.iloc[i]["Event Name"]
        url = new.iloc[i]["URL"]
        dat = new.iloc[i]["Date"]
        pocty.append(pocetstartujicich(z, dat, url))
    new["Starting"] = pocty
    new['Date'] = new['Date'].dt.strftime('%Y-%m-%d')
    return new[['Athlete', 'Event Name', 'Date', 'Rank', 'Starting']]

def pocetstartujicich(zavod, datum, raceid):
    novy = df.loc[(df['Event Name'] == zavod) & (df['Date'] == datum) & (df['URL'] == raceid)]
    return len(novy)

def najdityp(nazevzavodu):
    zavod = "FIS"
    if "European Cup" in nazevzavodu:
        zavod = "EC"
    if "Qualification" in nazevzavodu:
        zavod = "NE"
    if "Junior" in nazevzavodu:
        zavod = "JUN"
    if "FIS" in nazevzavodu:
        zavod = "FIS"
    if "World Cup" in nazevzavodu:
        zavod = "WC"
    if "World Championships" in nazevzavodu:
        zavod = "WCHAMP"
    if "World Championships" in nazevzavodu and "Junior" in nazevzavodu:
        zavod = "WJC"
    if "Youth Olympic" in nazevzavodu:
        zavod = "YOG"
    if "Youth Olympic" in nazevzavodu and "European" in nazevzavodu:
        zavod = "EYOF"
    if "World University" in nazevzavodu:
        zavod = "WUG"
    return zavod

    
def dejbody(misto, pocetlidi, typ):
    base = 0
    maximum = 0
    if typ == "FIS" or typ == "JUN":
        base = 0.5
    ## WUG - World University Games
    elif (typ == "EC") or (typ == "EYOF") or (typ == "YOG") or (typ == "WUG"):
        base = 2
    elif typ == "WC":
        base = 4
    elif typ == "WCHAMP" or typ == "WJC":
        base = 5
    print(int(pocetlidi / 2))
    ## -1 znamená DNS a 0 znamená DNF/DSQ
    if misto < (int(pocetlidi / 2) + 1) and misto > 0:
        maximum = base
        if misto == 1:
            maximum = base * 10
        elif misto == 2:
            maximum = base * 8
        elif misto == 3:
            maximum = base * 6
        elif misto < 9 and misto > 3:
            maximum = base * 4
        elif misto < 17 and misto > 8:
            maximum = base * 2
    return maximum
        
assert dejbody(1, 25, "WC") == 40, "Nefunguje WC"   
assert dejbody(8, 14, "FIS") == 0, "Neni v prvni pulce"

tabulkastypy = pd.read_excel('SCMnove.xlsx')
tabulkastypy["Type"] = tabulkastypy["Type"].astype(str)
tabulkastypy["Rank"] = tabulkastypy["Rank"].astype(int)    

def oboduj(tabulkastypy):
    body = []
    for i in range(tabulkastypy.shape[0]):
        r = tabulkastypy["Rank"].iloc[i]
        s = tabulkastypy["Starting"].iloc[i]
        t = tabulkastypy["Type"].iloc[i]
        body.append(dejbody(r, s, t))
    stejne = []
    for bod in body:
        stejne.append(float(bod))
    tabulkastypy.loc[:, "Points"] = stejne
    return tabulkastypy
    
def udelejtyp(tabulkastypy):
    typy = []
    for i in range(tabulkastypy.shape[0]):
        z = tabulkastypy["Event Name"].iloc[i]
        typy.append(najdityp(z))
    stejne = []
    for bod in typy:
        stejne.append(bod)
    tabulkastypy.loc[:, "Type"] = stejne
    return tabulkastypy

finalni = filtruj("TULACH Ondrej")
finalni = pd.DataFrame(finalni._append(filtruj("SONKOVA Klara"), 
                  ignore_index = True))
finalni = pd.DataFrame(finalni._append(filtruj("KLEIN Krystof"), 
                  ignore_index = True))
finalni = pd.DataFrame(finalni._append(filtruj("JECHOVA Linda"), 
                  ignore_index = True))
finalni = pd.DataFrame(finalni._append(filtruj("ZVIRECI Martina"), 
                  ignore_index = True))

tabulkastypy = oboduj(tabulkastypy)

finalni["Rank"] = finalni["Rank"].fillna(0)
finalni = udelejtyp(finalni)
finalni = finalni[finalni["Type"] != "NE"]
finalni = oboduj(finalni)

print(finalni)

finalni.to_excel("FullAutoSCM.xlsx")
tabulkastypy.to_excel("SCMnoveAutomaticke.xlsx")



