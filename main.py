import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# --- API AYARLARI ---
API_KEY = "fea9089b7fff416fb93151733e2063fa"
BASE_URL = "https://api.football-data.org/v4/competitions/{code}/matches"
HEADERS = {"X-Auth-Token": API_KEY}

# --- Lig Dictionary (code + renk + logo_path) ---
COMPETITIONS = {
# Premier League
"premier league": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},
"premier lig": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},
"Premier League": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},
"Premier league": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},
"pl": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},
"PL": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},
"Premier lig": {"code": "PL", "color": "#38003C", "logo": "logos/PremierLeague.png"},

# La Liga
"la liga": {"code": "PD", "color": "#FF4C00", "logo": "logos/Laliga.png"},
"La liga": {"code": "PD", "color": "#FF4C00", "logo": "logos/Laliga.png"},
"La Liga": {"code": "PD", "color": "#FF4C00", "logo": "logos/Laliga.png"},
"laliga": {"code": "PD", "color": "#FF4C00", "logo": "logos/LaLiga.png"},
"LaLiga": {"code": "PD", "color": "#FF4C00", "logo": "logos/Laliga.png"},
"pd": {"code": "PD", "color": "#FF4C00", "logo": "logos/LaLiga.png"},

# Şampiyonlar Ligi
"şampiyonlar ligi": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},
"Şampiyonlar Ligi": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},
"Champions League": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},
"Champions league": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},
"CL": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},
"champions league": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},
"cl": {"code": "CL", "color": "#1A237E", "logo": "logos/ChampionsLeague.png"},

# Serie A
"serie a": {"code": "SA", "color": "#0066B3", "logo": "logos/SeriaA.png"},
"sa": {"code": "SA", "color": "#0066B3", "logo": "logos/SeriaA.png"},
"Serie A": {"code": "SA", "color": "#0066B3", "logo": "logos/SeriaA.png"},
"Serie a": {"code": "SA", "color": "#0066B3", "logo": "logos/SeriaA.png"},


# Bundesliga
"bundesliga": {"code": "BL1", "color": "#DD0000", "logo": "logos/Bundesliga.png"},
"bl1": {"code": "BL1", "color": "#DD0000", "logo": "logos/Bundesliga.png"},
"Bundesliga": {"code": "BL1", "color": "#DD0000", "logo": "logos/Bundesliga.png"},

# Ligue 1
"ligue 1": {"code": "FL1", "color": "#123278", "logo": "logos/ligue1.png"},
"Ligue 1": {"code": "FL1", "color": "#123278", "logo": "logos/ligue1.png"},
"Ligue1": {"code": "FL1", "color": "#123278", "logo": "logos/ligue1.png"},
"ligue1": {"code": "FL1", "color": "#123278", "logo": "logos/ligue1.png"},
"fl1": {"code": "FL1", "color": "#123278", "logo": "logos/ligue1.png"},

# Süper Lig
"süper lig": {"code": "TUR", "color": "#E53935", "logo": "logos/SuperLig.png"},
"super lig": {"code": "TUR", "color": "#E53935", "logo": "logos/SuperLig.png"},
"tur": {"code": "TUR", "color": "#E53935", "logo": "logos/SuperLig.png"}
}

# --- Fonksiyon: Maçları getir ---
def fetch_matches():
    user_input = league_entry.get().strip().lower()
    if user_input not in COMPETITIONS:
        messagebox.showwarning("Uyarı", "Böyle bir lig bulunamadı!")
        return

    comp_info = COMPETITIONS[user_input]
    code, color, logo_path = comp_info["code"], comp_info["color"], comp_info["logo"]

    # Lig logosunu güncelle
    try:
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((80, 80))
        logo_photo = ImageTk.PhotoImage(logo_img)
        league_logo_label.config(image=logo_photo)
        league_logo_label.image = logo_photo
    except:
        league_logo_label.config(image='', text="Logo Yok")

    league_name_label.config(text=user_input.title())

    url = BASE_URL.format(code=code)
    today = datetime.today().date()
    last_week = today - timedelta(days=7)
    next_week = today + timedelta(days=7)
    params = {"dateFrom": str(last_week), "dateTo": str(next_week)}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            messagebox.showerror("Hata", f"API Hatası: {response.status_code}")
            return

        data = response.json()
        matches = data.get("matches", [])

        for widget in results_frame.winfo_children():
            widget.destroy()

        if not matches:
            tk.Label(results_frame, text="Bu hafta için maç bulunamadı.",
                     fg="white", bg=color, font=("Arial", 14)).pack(pady=5)
            return

        for m in matches:
            frame = tk.Frame(results_frame, bg=color, bd=2, relief="ridge")
            frame.pack(fill="x", pady=5, padx=10)

            home, away = m["homeTeam"]["name"], m["awayTeam"]["name"]
            status, utc_date = m["status"], m["utcDate"]
            score = m["score"]["fullTime"]
            score_text = f"{score['home']} - {score['away']}" if score['home'] is not None else "-"

            date_local = datetime.fromisoformat(utc_date.replace("Z", "+00:00")).strftime("%d.%m.%Y %H:%M")

            tk.Label(frame, text=f"{home} vs {away}", font=("Arial", 16, "bold"),
                     bg=color, fg="white").pack(side="left", padx=10)
            tk.Label(frame, text=score_text, font=("Arial", 16, "bold"),
                     bg=color, fg="yellow").pack(side="left", padx=10)
            tk.Label(frame, text=f"{status} | {date_local}", font=("Arial", 10),
                     bg=color, fg="lightgray").pack(side="right", padx=10)

    except Exception as e:
        messagebox.showerror("Hata", str(e))

# --- UI ---
window = tk.Tk()
window.title("SPRTS")
window.geometry("800x650")
window.config(bg="#222")

# En üstte genel logo
try:
    top_logo = Image.open("SPRT.png")
    top_logo = top_logo.resize((120, 120))
    top_logo_photo = ImageTk.PhotoImage(top_logo)
    top_logo_label = tk.Label(window, image=top_logo_photo, bg="#222")
    top_logo_label.image = top_logo_photo
    top_logo_label.pack(pady=10)
except:
    tk.Label(window, text="SPRT", bg="#222", fg="white", font=("Arial", 20, "bold")).pack(pady=10)

# Input alanı
tk.Label(window, text="Lig adı gir (ör: la liga, premier league, Şampiyonlar Ligi):",
         bg="#222", fg="white", font=("Arial", 12)).pack(pady=5)
league_entry = tk.Entry(window, width=40, font=("Arial", 12))
league_entry.pack(pady=5)

fetch_button = tk.Button(window, text="Maçları Getir", command=fetch_matches,
                         bg="#555", fg="white", font=("Arial", 12, "bold"))
fetch_button.pack(pady=10)

# Seçilen lig için logo + isim
header_frame = tk.Frame(window, bg="#222")
header_frame.pack(pady=10)

league_logo_label = tk.Label(header_frame, bg="#222")
league_logo_label.pack(side="left", padx=10)

league_name_label = tk.Label(header_frame, text="", bg="#222", fg="white", font=("Arial", 20, "bold"))
league_name_label.pack(side="left", padx=10)

# Scrollable results
canvas = tk.Canvas(window, bg="#222", highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#222")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

results_frame = scrollable_frame

window.mainloop()
