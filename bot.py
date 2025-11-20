# app.py
from flask import Flask, render_template_string, Response
import os
import json

app = Flask(__name__)

# GÜNCELLENMİŞ API VERİLERİ - YENİ ENDPOINT'LERLE
ALL_APIS = [
    # 🌐 NABI API - TÜM ENDPOINT'LER
    {"id": "yabanci", "title": "Yabancı Sorgulama", "icon": "🌍", "url": "https://nabi.api.org.totalh.net/yabanci?ad=JOHN&soyad=DOE", "desc": "Yabancı kişi sorgulama."},
    {"id": "cinsiyet", "title": "Cinsiyet Sorgulama", "icon": "⚧️", "url": "https://nabi.api.org.totalh.net/cinsiyet?tc=11111111111", "desc": "TC ile cinsiyet sorgulama."},
    {"id": "din", "title": "Din Sorgulama", "icon": "🕌", "url": "https://nabi.api.org.totalh.net/din?tc=11111111111", "desc": "TC ile din sorgulama."},
    {"id": "vergino", "title": "Vergi No Sorgulama", "icon": "💰", "url": "https://nabi.api.org.totalh.net/vergino?tc=11111111111", "desc": "TC ile vergi numarası sorgulama."},
    {"id": "medenihal", "title": "Medeni Hal Sorgulama", "icon": "💍", "url": "https://nabi.api.org.totalh.net/medenihal?tc=11111111111", "desc": "TC ile medeni hal sorgulama."},
    {"id": "koy", "title": "Köy Sorgulama", "icon": "🏞️", "url": "https://nabi.api.org.totalh.net/koy?tc=11111111111", "desc": "TC ile köy bilgisi sorgulama."},
    {"id": "burc", "title": "Burç Sorgulama", "icon": "♈", "url": "https://nabi.api.org.totalh.net/burc?tc=11111111111", "desc": "TC ile burç sorgulama."},
    {"id": "kimlikkayit", "title": "Kimlik Kayıt Sorgulama", "icon": "📋", "url": "https://nabi.api.org.totalh.net/kimlikkayit?tc=11111111111", "desc": "TC ile kimlik kaydı sorgulama."},
    {"id": "dogumyeri", "title": "Doğum Yeri Sorgulama", "icon": "📍", "url": "https://nabi.api.org.totalh.net/dogumyeri?tc=11111111111", "desc": "TC ile doğum yeri sorgulama."},
    {"id": "yetimlik", "title": "Yetimlik Sorgulama", "icon": "👶", "url": "https://nabi.api.org.totalh.net/yetimlik?babatc=11111111111", "desc": "Baba TC ile yetimlik sorgulama."},

    # 👨‍👩‍👧‍👦 AİLE SORGULARI
    {"id": "kardes", "title": "Kardeş Sorgulama", "icon": "👥", "url": "https://nabi.api.org.totalh.net/kardes?tc=11111111111", "desc": "TC ile kardeş sorgulama."},
    {"id": "anne", "title": "Anne Sorgulama", "icon": "👩", "url": "https://nabi.api.org.totalh.net/anne?tc=11111111111", "desc": "TC ile anne sorgulama."},
    {"id": "baba", "title": "Baba Sorgulama", "icon": "👨", "url": "https://nabi.api.org.totalh.net/baba?tc=11111111111", "desc": "TC ile baba sorgulama."},
    {"id": "cocuklar", "title": "Çocuklar Sorgulama", "icon": "👶", "url": "https://nabi.api.org.totalh.net/cocuklar?tc=11111111111", "desc": "TC ile çocuklar sorgulama."},
    {"id": "amca", "title": "Amca Sorgulama", "icon": "👨", "url": "https://nabi.api.org.totalh.net/amca?tc=11111111111", "desc": "TC ile amca sorgulama."},
    {"id": "dayi", "title": "Dayı Sorgulama", "icon": "👨", "url": "https://nabi.api.org.totalh.net/dayi?tc=11111111111", "desc": "TC ile dayı sorgulama."},
    {"id": "hala", "title": "Hala Sorgulama", "icon": "👩", "url": "https://nabi.api.org.totalh.net/hala?tc=11111111111", "desc": "TC ile hala sorgulama."},
    {"id": "teyze", "title": "Teyze Sorgulama", "icon": "👩", "url": "https://nabi.api.org.totalh.net/teyze?tc=11111111111", "desc": "TC ile teyze sorgulama."},
    {"id": "kuzen", "title": "Kuzen Sorgulama", "icon": "👥", "url": "https://nabi.api.org.totalh.net/kuzen?tc=11111111111", "desc": "TC ile kuzen sorgulama."},
    {"id": "dede", "title": "Dede Sorgulama", "icon": "👴", "url": "https://nabi.api.org.totalh.net/dede?tc=11111111111", "desc": "TC ile dede sorgulama."},
    {"id": "nine", "title": "Nine Sorgulama", "icon": "👵", "url": "https://nabi.api.org.totalh.net/nine?tc=11111111111", "desc": "TC ile nine sorgulama."},
    {"id": "yeniden", "title": "Yeniden Sorgulama", "icon": "🔄", "url": "https://nabi.api.org.totalh.net/yeniden?tc=11111111111", "desc": "TC ile yeniden sorgulama."},

    # 🐍 SAHMARAN BOTU SORGULARI
    {"id": "sorgu", "title": "Ad Soyad Sorgulama", "icon": "🔍", "url": "https://nabi.api.org.totalh.net/sorgu?ad=AHMET&soyad=YILMAZ", "desc": "Ad soyad ile kişi sorgulama."},
    {"id": "aile", "title": "Aile Sorgulama", "icon": "👨‍👩‍👧‍👦", "url": "https://nabi.api.org.totalh.net/aile?tc=11111111111", "desc": "TC ile aile sorgulama."},
    {"id": "adres", "title": "Adres Sorgulama", "icon": "🏠", "url": "https://nabi.api.org.totalh.net/adres?tc=11111111111", "desc": "TC ile adres sorgulama."},
    {"id": "tc", "title": "TC Sorgulama", "icon": "🆔", "url": "https://nabi.api.org.totalh.net/tc?tc=11111111111", "desc": "TC kimlik sorgulama."},
    {"id": "gsmtc", "title": "GSM TC Sorgulama", "icon": "📱", "url": "https://nabi.api.org.totalh.net/gsmtc?gsm=5551112233", "desc": "GSM ile TC sorgulama."},
    {"id": "tcgsm", "title": "TC GSM Sorgulama", "icon": "📞", "url": "https://nabi.api.org.totalh.net/tcgsm?tc=11111111111", "desc": "TC ile GSM sorgulama."},
    {"id": "olumtarihi", "title": "Ölüm Tarihi Sorgulama", "icon": "💀", "url": "https://nabi.api.org.totalh.net/olumtarihi?tc=11111111111", "desc": "TC ile ölüm tarihi sorgulama."},
    {"id": "sulale", "title": "Sülale Sorgulama", "icon": "🌳", "url": "https://nabi.api.org.totalh.net/sulale?tc=11111111111", "desc": "TC ile sülale sorgulama."},
    {"id": "sms", "title": "SMS Sorgulama", "icon": "💬", "url": "https://nabi.api.org.totalh.net/sms?gsm=5551112233", "desc": "GSM ile SMS sorgulama."},
    {"id": "kizliksoyad", "title": "Kızlık Soyadı Sorgulama", "icon": "👰", "url": "https://nabi.api.org.totalh.net/kizliksoyad?tc=11111111111", "desc": "TC ile kızlık soyadı sorgulama."},
    {"id": "yas", "title": "Yaş Sorgulama", "icon": "🎂", "url": "https://nabi.api.org.totalh.net/yas?tc=11111111111", "desc": "TC ile yaş sorgulama."},
    {"id": "hikaye", "title": "Hikaye Sorgulama", "icon": "📖", "url": "https://nabi.api.org.totalh.net/hikaye?tc=11111111111", "desc": "TC ile hikaye sorgulama."},
    {"id": "sirano", "title": "Sıra No Sorgulama", "icon": "#️⃣", "url": "https://nabi.api.org.totalh.net/sirano?tc=11111111111", "desc": "TC ile sıra no sorgulama."},
    {"id": "ayakno", "title": "Ayak No Sorgulama", "icon": "🦶", "url": "https://nabi.api.org.totalh.net/ayakno?tc=11111111111", "desc": "TC ile ayak no sorgulama."},
    {"id": "operator", "title": "Operatör Sorgulama", "icon": "📶", "url": "https://nabi.api.org.totalh.net/operator?gsm=5551112233", "desc": "GSM ile operatör sorgulama."},
    {"id": "yegen", "title": "Yeğen Sorgulama", "icon": "👶", "url": "https://nabi.api.org.totalh.net/yegen?tc=11111111111", "desc": "TC ile yeğen sorgulama."},
    {"id": "cocuk", "title": "Çocuk Sorgulama", "icon": "👶", "url": "https://nabi.api.org.totalh.net/cocuk?tc=11111111111", "desc": "TC ile çocuk sorgulama."},

    # 🐱 MİYAVREM BOTU SORGULARI
    {"id": "vesika", "title": "Vesika Sorgulama", "icon": "🪪", "url": "https://nabi.api.org.totalh.net/vesika?tc=11111111111", "desc": "TC ile vesika sorgulama."},
    {"id": "plaka", "title": "Plaka Sorgulama", "icon": "🚗", "url": "https://nabi.api.org.totalh.net/plaka?plaka=34ABC123", "desc": "Plaka ile araç sorgulama."},
    {"id": "tcplaka", "title": "TC Plaka Sorgulama", "icon": "🚙", "url": "https://nabi.api.org.totalh.net/tcplaka?tc=11111111111", "desc": "TC ile plaka sorgulama."},

    # 🌤️ TASSAKLI REAL BOTU - HAVA DURUMU & KUR
    {"id": "hava", "title": "Hava Durumu", "icon": "🌤️", "url": "https://nabi.api.org.totalh.net/hava?sehir=Istanbul", "desc": "Şehir ile hava durumu sorgulama."},
    {"id": "kur", "title": "Kur Sorgulama", "icon": "💹", "url": "https://nabi.api.org.totalh.net/kur", "desc": "Döviz kurları sorgulama."},

    # 🎮 TASSAKLI REAL BOTU - OYUN KODLARI
    {"id": "steam_kod", "title": "Steam Kod", "icon": "🎮", "url": "https://nabi.api.org.totalh.net/steam_kod", "desc": "Steam kod sorgulama."},
    {"id": "vp_kod", "title": "VP Kod", "icon": "🕹️", "url": "https://nabi.api.org.totalh.net/vp_kod", "desc": "VP kod sorgulama."},
    {"id": "play_kod", "title": "Play Kod", "icon": "🎯", "url": "https://nabi.api.org.totalh.net/play_kod", "desc": "Play kod sorgulama."},
    {"id": "uc_kod", "title": "UC Kod", "icon": "📱", "url": "https://nabi.api.org.totalh.net/uc_kod", "desc": "UC kod sorgulama."},
    {"id": "mlbb_kod", "title": "MLBB Kod", "icon": "⚔️", "url": "https://nabi.api.org.totalh.net/mlbb_kod", "desc": "MLBB kod sorgulama."},
    {"id": "kazandiriyo", "title": "Kazandırıyor", "icon": "🎁", "url": "https://nabi.api.org.totalh.net/kazandiriyo", "desc": "Kazandırıyor sorgulama."},
    {"id": "robux_kod", "title": "Robux Kod", "icon": "🤖", "url": "https://nabi.api.org.totalh.net/robux_kod", "desc": "Robux kod sorgulama."},
    {"id": "nitro", "title": "Nitro", "icon": "⚡", "url": "https://nabi.api.org.totalh.net/nitro", "desc": "Nitro sorgulama."},
    {"id": "coctas", "title": "Coctas", "icon": "🍹", "url": "https://nabi.api.org.totalh.net/coctas", "desc": "Coctas sorgulama."},
    {"id": "freefire", "title": "Free Fire", "icon": "🔥", "url": "https://nabi.api.org.totalh.net/freefire", "desc": "Free Fire sorgulama."},

    # 💳 TASSAKLI REAL BOTU - KART & HESAP BİLGİLERİ
    {"id": "free", "title": "Free Kart", "icon": "💳", "url": "https://nabi.api.org.totalh.net/free", "desc": "Free kart sorgulama."},
    {"id": "live", "title": "Live Kart", "icon": "💳", "url": "https://nabi.api.org.totalh.net/live", "desc": "Live kart sorgulama."},
    {"id": "troy", "title": "Troy Kart", "icon": "💳", "url": "https://nabi.api.org.totalh.net/troy", "desc": "Troy kart sorgulama."},

    # 🔐 TASSAKLI REAL BOTU - HESAP BİLGİLERİ
    {"id": "midasbuy", "title": "Midas Buy", "icon": "🛒", "url": "https://nabi.api.org.totalh.net/midasbuy", "desc": "Midas buy hesap sorgulama."},
    {"id": "predunyam", "title": "Predünya", "icon": "🌎", "url": "https://nabi.api.org.totalh.net/predunyam", "desc": "Predünya hesap sorgulama."},
    {"id": "smsonay", "title": "SMS Onay", "icon": "📲", "url": "https://nabi.api.org.totalh.net/smsonay", "desc": "SMS onay hesap sorgulama."},
    {"id": "zara", "title": "Zara", "icon": "👗", "url": "https://nabi.api.org.totalh.net/zara", "desc": "Zara hesap sorgulama."},
    {"id": "exxen", "title": "Exxen", "icon": "📺", "url": "https://nabi.api.org.totalh.net/exxen", "desc": "Exxen hesap sorgulama."},
    {"id": "blutv", "title": "BluTV", "icon": "📺", "url": "https://nabi.api.org.totalh.net/blutv", "desc": "BluTV hesap sorgulama."},
    {"id": "amazon", "title": "Amazon", "icon": "📦", "url": "https://nabi.api.org.totalh.net/amazon", "desc": "Amazon hesap sorgulama."},
    {"id": "purna", "title": "Purna", "icon": "🛍️", "url": "https://nabi.api.org.totalh.net/purna", "desc": "Purna hesap sorgulama."},
    {"id": "carparking", "title": "Car Parking", "icon": "🚗", "url": "https://nabi.api.org.totalh.net/carparking", "desc": "Car Parking hesap sorgulama."},
    {"id": "roblox", "title": "Roblox", "icon": "🎮", "url": "https://nabi.api.org.totalh.net/roblox", "desc": "Roblox hesap sorgulama."},
    {"id": "twitter", "title": "Twitter", "icon": "🐦", "url": "https://nabi.api.org.totalh.net/twitter", "desc": "Twitter hesap sorgulama."},
    {"id": "netflix", "title": "Netflix", "icon": "🎬", "url": "https://nabi.api.org.totalh.net/netflix", "desc": "Netflix hesap sorgulama."},
    {"id": "pubg", "title": "PUBG", "icon": "🎯", "url": "https://nabi.api.org.totalh.net/pubg", "desc": "PUBG hesap sorgulama."},
    {"id": "hepsiburada", "title": "Hepsiburada", "icon": "🛒", "url": "https://nabi.api.org.totalh.net/hepsiburada", "desc": "Hepsiburada hesap sorgulama."},
    {"id": "hotmail", "title": "Hotmail", "icon": "📧", "url": "https://nabi.api.org.totalh.net/hotmail", "desc": "Hotmail hesap sorgulama."},
    {"id": "valorant", "title": "Valorant", "icon": "🎮", "url": "https://nabi.api.org.totalh.net/valorant", "desc": "Valorant hesap sorgulama."},
    {"id": "facebook", "title": "Facebook", "icon": "📘", "url": "https://nabi.api.org.totalh.net/facebook", "desc": "Facebook hesap sorgulama."},
    {"id": "spotify", "title": "Spotify", "icon": "🎵", "url": "https://nabi.api.org.totalh.net/spotify", "desc": "Spotify hesap sorgulama."},
    {"id": "epicgame", "title": "Epic Games", "icon": "🎮", "url": "https://nabi.api.org.totalh.net/epicgame", "desc": "Epic Games hesap sorgulama."},
    {"id": "blizzard", "title": "Blizzard", "icon": "❄️", "url": "https://nabi.api.org.totalh.net/blizzard", "desc": "Blizzard hesap sorgulama."},

    # 😊 TASSAKLI REAL BOTU - EĞLENCE
    {"id": "kalp", "title": "Kalp", "icon": "💖", "url": "https://nabi.api.org.totalh.net/kalp", "desc": "Kalp sorgulama."},
    {"id": "sigma", "title": "Sigma", "icon": "σ", "url": "https://nabi.api.org.totalh.net/sigma", "desc": "Sigma sorgulama."},
    {"id": "anime", "title": "Anime", "icon": "🎌", "url": "https://nabi.api.org.totalh.net/anime", "desc": "Anime sorgulama."},
    {"id": "imposter", "title": "Imposter", "icon": "👤", "url": "https://nabi.api.org.totalh.net/imposter", "desc": "Imposter sorgulama."},
    {"id": "ask", "title": "Aşk", "icon": "💘", "url": "https://nabi.api.org.totalh.net/ask", "desc": "Aşk sorgulama."},
    {"id": "dart", "title": "Dart", "icon": "🎯", "url": "https://nabi.api.org.totalh.net/dart", "desc": "Dart sorgulama."},
    {"id": "zar", "title": "Zar", "icon": "🎲", "url": "https://nabi.api.org.totalh.net/zar", "desc": "Zar sorgulama."},

    # 🛠️ DİĞER ENDPOINT'LER
    {"id": "saglik", "title": "Sağlık Sorgulama", "icon": "🏥", "url": "https://nabi.api.org.totalh.net/saglik", "desc": "Sağlık sorgulama."},
    {"id": "raw", "title": "Raw Sorgulama", "icon": "📊", "url": "https://nabi.api.org.totalh.net/raw?tc=11111111111", "desc": "TC ile raw sorgulama."},
    {"id": "root", "title": "Ana Sayfa", "icon": "🏠", "url": "https://nabi.api.org.totalh.net/", "desc": "Ana sayfa endpoint."},

    # 🔵 İHBAR API'LERİ
    {"id": "usomihbar", "title": "USOM İhbar", "icon": "🔵", "url": "https://nabisystem.ihbar.org.totalh.net/usomihbar?adres=Köy&yolu&mevkii&detay=kavga&sesleri&duyuluyor", "desc": "USOM ihbar gönderme."},
    {"id": "egmihbar", "title": "EGM İhbar", "icon": "👮", "url": "https://nabisystem.ihbar.org.totalh.net/egmihbar?adres=İstanbul&Kadıköy&detay=Şüpheli&biri&var", "desc": "EGM (Polis) ihbar gönderme."},
    {"id": "jandarmaihbar", "title": "Jandarma İhbar", "icon": "🎖️", "url": "https://nabisystem.ihbar.org.totalh.net/jandarmaihbar?adres=Dağlık&bölge&mevkii&detay=kavga&sesi&geliyor", "desc": "Jandarma ihbar gönderme."}
]

# HTML template (aynı template, sadece API'ler değişti)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nabi System API Servisi — v2</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root{
  --bg-1:#0f1724;--bg-2:#0b1220;--accent-1:#4cc9f0;--accent-2:#ff8a00;
  --glass:rgba(255,255,255,0.06);--card-border:rgba(255,255,255,0.06);--muted:#cbd5e1;
  --glass-blur:10px;--radius:14px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,Arial;background:radial-gradient(1200px 600px at 10% 10%, rgba(76,201,240,0.06), transparent), linear-gradient(135deg,var(--bg-1) 0%,var(--bg-2) 100%);color:#fff;min-height:100vh;padding:16px;position:relative}
.bg-image{position:fixed;inset:0;background-image:url('https://i.ibb.co/wNDn84h0/file-00000000ffc061f4bacedf89d0e6a130.png');background-size:cover;background-position:center;opacity:0.55;z-index:-3;filter:grayscale(10%);transition:filter .35s ease, opacity .35s ease}
.bg-image.blurred{filter:blur(6px) saturate(0.75);opacity:0.46}
.gradient-overlay{position:fixed;inset:0;z-index:-2;background:linear-gradient(90deg, rgba(255,140,0,0.06), rgba(76,201,240,0.04));mix-blend-mode:overlay;pointer-events:none}
.wrapper{max-width:1200px;margin:0 auto}
header{display:flex;flex-direction:column;gap:16px;margin-bottom:20px}
.brand h1{font-size:24px;font-weight:800;background:linear-gradient(90deg,var(--accent-2),#e52e71);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header-top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.controls{display:flex;gap:10px;align-items:center}
.search{display:flex;align-items:center;background:var(--glass);padding:8px 12px;border-radius:12px;border:1px solid var(--card-border);gap:8px;flex:1;min-width:200px;max-width:400px}
.search input{background:transparent;border:0;outline:0;color:inherit;font-size:14px;width:100%}
.small-btn{background:transparent;border:1px solid var(--card-border);padding:8px 10px;border-radius:10px;font-size:13px;cursor:pointer}
.stats{display:flex;gap:10px;align-items:center}
.stat{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:8px 12px;border-radius:10px;border:1px solid var(--card-border);font-weight:600}
.api-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:12px}
.api-card{background:var(--glass);padding:14px;border-radius:var(--radius);border:1px solid var(--card-border);backdrop-filter:blur(var(--glass-blur));display:flex;flex-direction:column;gap:10px}
.api-head{display:flex;align-items:flex-start;gap:10px}
.api-icon{width:42px;height:42px;border-radius:8px;display:grid;place-items:center;font-size:18px;background:linear-gradient(135deg,#4361ee,#3a0ca3)}
.api-title{font-weight:700;color:#ff6aa2;font-size:14px;cursor:pointer}
.api-desc{font-size:12px;color:var(--muted)}
.api-url{background:rgba(0,0,0,0.3);padding:8px 10px;border-radius:8px;font-family:monospace;font-size:11px;color:var(--accent-1);word-break:break-all;border:1px solid rgba(255,255,255,0.04);cursor:pointer}
.card-actions{display:flex;gap:6px;flex-wrap:wrap}
.btn{padding:6px 8px;border-radius:8px;border:1px solid var(--card-border);background:transparent;color:#fff;cursor:pointer}
.badge{padding:4px 8px;border-radius:999px;background:rgba(40,167,69,0.18);color:#b7f0c1;font-weight:700;font-size:11px}
.toast{position:fixed;right:12px;bottom:12px;background:#0b1220;padding:8px 12px;border-radius:8px;border:1px solid var(--card-border);display:none;z-index:50;font-size:13px}
@media (max-width:768px){.api-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
    <div class="bg-image" id="bgImage"></div>
    <div class="gradient-overlay"></div>

    <div class="wrapper">
        <header>
            <div class="header-top">
                <div>
                    <h1>Nabi System</h1>
                    <div style="color:var(--muted);font-size:13px">API Service • Mobile Uyumlu</div>
                </div>
                <div class="controls">
                    <div class="stats">
                        <div class="stat"><div style="font-size:16px">{{ total }}</div><div style="font-size:11px;color:var(--muted)">Toplam API</div></div>
                    </div>
                </div>
            </div>

            <div style="display:flex;gap:8px;margin-top:10px;align-items:center">
                <div class="search">
                    <i class="fa fa-search" style="opacity:0.7;margin-right:8px"></i>
                    <input id="q" placeholder="API ara..." onkeyup="searchApis()" />
                </div>
                <button class="small-btn" onclick="toggleBackground()">BG</button>
                <button class="btn" onclick="downloadAll()"><i class="fa fa-download"></i> Tüm API'leri JSON indir</button>
            </div>
        </header>

        <main>
            <div style="background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);color:var(--muted);margin-bottom:12px">
                <i class="fa fa-exclamation-triangle" style="color:#ffb4b4;margin-right:8px"></i>
                Apiler bize aittir. Lütfen verileri paylaşırken gizlilik ve yasalara dikkat ediniz.
            </div>

            <h2 style="color:var(--accent-1);margin-bottom:8px">🚀 TÜM API LİSTESİ ({{ total }} API)</h2>
            <div class="api-grid" id="allApisGrid">
                {% for api in apis %}
                <div class="api-card" data-text="{{ (api.id ~ ' ' ~ api.title ~ ' ' ~ api.desc ~ ' ' ~ api.url)|lower|e }}" data-url="{{ api.url|e }}">
                    <div class="api-head">
                        <div class="api-icon">{{ api.icon }}</div>
                        <div style="flex:1">
                            <div class="api-title" onclick="copyToClipboard(this.closest('.api-card').dataset.url)">{{ api.title }}</div>
                            <div class="api-desc">{{ api.desc }}</div>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px">
                            <div class="badge">Aktif</div>
                        </div>
                    </div>

                    <div class="api-url" onclick="copyToClipboard(this.closest('.api-card').dataset.url)">{{ api.url }}</div>

                    <div class="card-actions">
                        <button class="btn" onclick="copyToClipboard(this.closest('.api-card').dataset.url)"><i class="fa fa-copy"></i> Kopyala</button>
                        <button class="btn" onclick="openUrl(this.closest('.api-card').dataset.url)"><i class="fa fa-arrow-up-right-from-square"></i> Aç</button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </main>

        <footer>
            <div>NABI SYSTEM SUNAR — v2 • {{ total }} API • Mobile Uyumlu</div>
            <div style="margin-top:6px;font-size:11px">© 2025 Nabi System • Telegram: @sukazatkinis</div>
        </footer>
    </div>

    <div class="toast" id="toast">Kopyalandı!</div>

<script>
function searchApis() {
    const q = document.getElementById('q').value.toLowerCase();
    document.querySelectorAll('[data-text]').forEach(el=>{
        el.style.display = el.dataset.text.includes(q) ? '' : 'none';
    });
}

async function copyToClipboard(text) {
    if (!text) return showToast('Kopyalanacak metin yok');
    try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(text);
        } else {
            // fallback
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
        }
        showToast('URL kopyalandı!');
    } catch (e) {
        console.error(e);
        showToast('Kopyalama başarısız');
    }
}

function openUrl(url) {
    if (!url) return showToast('Açılacak adres yok');
    // Eğer url "curl " ile başlıyorsa, curl komutunu dosya olarak indir
    if (url.trim().toLowerCase().startsWith('curl ')) {
        const filename = 'command.txt';
        const blob = new Blob([url], {type: 'text/plain;charset=utf-8'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(a.href);
        a.remove();
        showToast('Komut indiriliyor...');
        return;
    }
    try {
        // normal URL aç
        window.open(url, '_blank');
    } catch (e) {
        // fallback: data URL ile aç
        const a = document.createElement('a');
        a.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(url);
        a.target = '_blank';
        document.body.appendChild(a);
        a.click();
        a.remove();
    }
}

async function downloadAll() {
    try {
        const resp = await fetch('/api-list');
        if (!resp.ok) throw new Error('İndirilemedi');
        const blob = await resp.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'apis.json';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(a.href);
        a.remove();
        showToast('apis.json indiriliyor...');
    } catch (e) {
        console.error(e);
        showToast('İndirme başarısız');
    }
}

function toggleBackground() {
    document.getElementById('bgImage').classList.toggle('blurred');
}

function showToast(msg) {
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.style.display = 'block';
    clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(()=>{ t.style.display = 'none'; }, 1500);
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, apis=ALL_APIS, total=len(ALL_APIS))

@app.route("/api-list")
def api_list():
    return Response(json.dumps({"total": len(ALL_APIS), "apis": ALL_APIS}, ensure_ascii=False, indent=2),
                    content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # geliştirme için debug True, production da False + gunicorn + nginx önerilir
    app.run(host="0.0.0.0", port=port, debug=True)
