"""
╔══════════════════════════════════════════════════════════╗
║          BUSZIN — Tamil Nadu Bus Booking System          ║
║              Double-click to launch the app              ║
╚══════════════════════════════════════════════════════════╝

Requirements: Python 3.8+  (tkinter is included with Python)
Optional:     pip install tkinterweb   ← for in-app browser window
"""

import os, sys, threading, time, socket, webbrowser, tempfile, json
from http.server import HTTPServer, BaseHTTPRequestHandler
import tkinter as tk
from tkinter import ttk, font, messagebox
from PIL import Image, ImageTk
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Deployment working!"


# ─────────────────────────── EMBEDDED HTML APP ───────────────────────────────
HTML_APP = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BUSZIN — Tamil Nadu Bus Booking</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --saffron:#FF6B00; --saffron-light:#FF8C00; --saffron-pale:#FFF3E0;
    --green-dark:#1B5E20; --green-mid:#2E7D32; --green-light:#E8F5E9;
    --cream:#FAFAF7; --charcoal:#1A1A2E; --slate:#4A4A6A; --muted:#8A8AA0;
    --border:rgba(0,0,0,0.08); --white:#FFFFFF; --danger:#D32F2F; --success:#2E7D32; --gold:#F9A825;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background: url('images/dashboard.jpg') no-repeat center center fixed;
  background-size: cover;font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--charcoal);overflow-x:hidden;}
  h1,h2,h3{font-family:'Playfair Display',serif;}

  /* ── AUTH ── */
  #auth-screen{min-height:100vh;display:flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 40%,#FF6B00 100%);position:relative;overflow:hidden;}
  #auth-screen::before{content:'';position:absolute;inset:0;
    background:url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="40" fill="%23ffffff08"/><circle cx="80" cy="80" r="60" fill="%23ffffff05"/></svg>');}
  .auth-card{background:white;border-radius:20px;padding:48px 40px;width:420px;max-width:90vw;
    position:relative;z-index:1;box-shadow:0 40px 80px rgba(0,0,0,0.3);}
  .auth-logo{text-align:center;margin-bottom:32px;}
  .auth-logo .logo-icon{width:64px;height:64px;background:linear-gradient(135deg,#FF6B00,#FF8C00);
    border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 12px;}
  .auth-logo h1{font-size:28px;color:var(--charcoal);}
  .auth-logo p{color:var(--muted);font-size:14px;margin-top:4px;}
  .auth-tabs{display:flex;background:#F5F5F5;border-radius:12px;padding:4px;margin-bottom:28px;}
  .auth-tab{flex:1;padding:10px;text-align:center;border-radius:8px;cursor:pointer;
    font-size:14px;font-weight:500;color:var(--muted);transition:all .2s;}
  .auth-tab.active{background:white;color:var(--charcoal);box-shadow:0 2px 8px rgba(0,0,0,0.1);}
  .form-group{margin-bottom:16px;}
  .form-group label{display:block;font-size:13px;font-weight:500;color:var(--slate);margin-bottom:6px;}
  .form-group input{width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;
    font-size:14px;font-family:'DM Sans',sans-serif;transition:border-color .2s;outline:none;background:#FAFAFA;}
  .form-group input:focus{border-color:var(--saffron);background:white;}
  .btn-primary{width:100%;padding:14px;background:linear-gradient(135deg,var(--saffron),var(--saffron-light));
    color:white;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;
    font-family:'DM Sans',sans-serif;transition:transform .1s,box-shadow .2s;}
  .btn-primary:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(255,107,0,0.4);}
  .auth-error{color:var(--danger);font-size:13px;margin-top:8px;min-height:18px;}

  /* ── NAVBAR ── */
  #app{display:none;min-height:100vh;flex-direction:column;}
  .navbar{background:white;border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;
    box-shadow:0 2px 20px rgba(0,0,0,0.08);}
  .nav-inner{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;gap:8px;height:64px;}
  .nav-logo{font-family:'Playfair Display',serif;font-size:22px;color:var(--saffron);font-weight:700;
    margin-right:auto;display:flex;align-items:center;gap:8px;}
  .nav-btn{padding:9px 18px;border:none;background:transparent;border-radius:8px;font-size:14px;
    font-weight:500;color:var(--slate);cursor:pointer;font-family:'DM Sans',sans-serif;
    transition:all .2s;white-space:nowrap;}
  .nav-btn:hover{background:var(--saffron-pale);color:var(--saffron);}
  .nav-btn.active{background:var(--saffron);color:white;}
  .nav-user{display:flex;align-items:center;gap:8px;margin-left:16px;padding-left:16px;border-left:1px solid var(--border);}
  .nav-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--green-mid),var(--green-dark));
    display:flex;align-items:center;justify-content:center;color:white;font-size:13px;font-weight:600;}
  .nav-user-name{font-size:13px;font-weight:500;color:var(--slate);}
  .btn-logout{padding:7px 14px;border:1.5px solid var(--border);background:transparent;border-radius:8px;
    font-size:13px;color:var(--muted);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;}
  .btn-logout:hover{border-color:var(--danger);color:var(--danger);}

  /* ── PAGES ── */
  .page{display:none;flex:1;}
  .page.active{display:block;}

  /* ── HOME / HERO ── */
  .hero{height:480px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;}
  .hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background: linear-gradient(
      rgba(0,0,0,0.4),
      rgba(0,0,0,0.6)
    ),
    url("/images/dashboard.jpg");

  background-size: cover;
  background-position: center;
  z-index: -1;
}
  .hero-pattern{position:absolute;inset:0;opacity:.08;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Ccircle cx='30' cy='30' r='20' fill='none' stroke='white' stroke-width='1'/%3E%3C/svg%3E") repeat;}
  .hero-content{position:relative;text-align:center;color:white;padding:0 24px;}
  .hero-content h1{font-size:52px;font-weight:700;line-height:1.1;text-shadow:0 2px 20px rgba(0,0,0,0.3);}
  .hero-content p{font-size:18px;margin-top:12px;opacity:.9;font-family:'DM Sans';font-weight:300;}
  .hero-badge{display:inline-block;background:rgba(255,255,255,0.2);backdrop-filter:blur(10px);
    border:1px solid rgba(255,255,255,0.3);border-radius:30px;padding:8px 20px;font-size:13px;
    margin-bottom:20px;letter-spacing:.5px;}
  

  /* ── BOOKING ── */
  .booking-page{max-width:900px;margin:0 auto;padding:48px 24px;}
  .booking-page h2{font-size:32px;margin-bottom:8px;}
  .booking-page .sub{color:var(--muted);margin-bottom:40px;}
  .booking-form-card{background:white;border-radius:20px;padding:36px;
    box-shadow:0 4px 24px rgba(0,0,0,0.08);margin-bottom:32px;}
  .input-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;align-items:end;}
  .field-wrap{position:relative;}
  .field-label{font-size:13px;font-weight:500;color:var(--slate);margin-bottom:6px;display:block;}
  .field-input{width:100%;padding:13px 16px;border:1.5px solid var(--border);border-radius:12px;
    font-size:14px;font-family:'DM Sans';outline:none;transition:border-color .2s;background:#FAFAFA;}
  .field-input:focus{border-color:var(--saffron);background:white;}
  .autocomplete-list{position:absolute;top:calc(100% + 4px);left:0;right:0;background:white;
    border:1.5px solid var(--border);border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.12);
    z-index:200;overflow:hidden;display:none;max-height:240px;overflow-y:auto;}
  .autocomplete-item{padding:11px 16px;cursor:pointer;font-size:14px;color:var(--charcoal);
    transition:background .15s;border-bottom:1px solid #F5F5F5;display:flex;align-items:center;gap:8px;}
  .autocomplete-item:hover{background:var(--saffron-pale);color:var(--saffron);}
  .autocomplete-item:last-child{border-bottom:none;}
  .btn-search{padding:13px 24px;background:linear-gradient(135deg,var(--saffron),var(--saffron-light));
    color:white;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;
    font-family:'DM Sans';transition:all .2s;white-space:nowrap;}
  .btn-search:hover{box-shadow:0 8px 24px rgba(255,107,0,0.4);transform:translateY(-1px);}

  /* ── BUS RESULTS ── */
  .results-section{animation:fadeUp .4s ease;}
  @keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
  .results-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;}
  .results-header h3{font-size:20px;}
  .results-count{background:var(--saffron-pale);color:var(--saffron);padding:4px 12px;border-radius:20px;
    font-size:13px;font-weight:500;}
  .bus-card{background:white;border-radius:16px;padding:24px 28px;margin-bottom:16px;
    box-shadow:0 2px 12px rgba(0,0,0,0.06);transition:box-shadow .2s;display:flex;
    align-items:center;gap:24px;border:1.5px solid transparent;}
  .bus-card:hover{box-shadow:0 8px 28px rgba(0,0,0,0.12);border-color:var(--saffron);}
  .bus-logo{width:56px;height:56px;border-radius:12px;display:flex;align-items:center;
    justify-content:center;font-size:22px;flex-shrink:0;}
  .bus-info{flex:1;}
  .bus-name{font-size:17px;font-weight:600;color:var(--charcoal);}
  .bus-type{font-size:12px;color:var(--muted);margin-top:2px;}
  .bus-times{display:flex;align-items:center;gap:16px;margin-top:12px;}
  .time-block{text-align:center;}
  .time-big{font-size:22px;font-weight:600;color:var(--charcoal);}
  .time-label{font-size:12px;color:var(--muted);}
  .duration-line{display:flex;flex-direction:column;align-items:center;gap:4px;}
  .dur-line{width:80px;height:2px;background:linear-gradient(90deg,var(--saffron),var(--green-mid));border-radius:2px;}
  .dur-text{font-size:12px;color:var(--muted);}
  .bus-fare{text-align:right;}
  .fare-price{font-size:26px;font-weight:700;color:var(--saffron);}
  .fare-label{font-size:12px;color:var(--muted);}
  .fare-seats{font-size:13px;color:var(--success);font-weight:500;margin-top:4px;}
  .btn-book{padding:11px 24px;background:var(--saffron);color:white;border:none;border-radius:10px;
    font-size:14px;font-weight:600;cursor:pointer;font-family:'DM Sans';transition:all .2s;margin-left:16px;}
  .btn-book:hover{background:#E65100;transform:translateY(-1px);}
  .bus-amenities{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;}
  .amenity{background:#F5F5F5;border-radius:6px;padding:3px 8px;font-size:11px;color:var(--slate);}

  /* ── SEATS ── */
  .seat-page{max-width:900px;margin:0 auto;padding:48px 24px;}
  .seat-page h2{font-size:32px;margin-bottom:8px;}
  .journey-info-bar{background:white;border-radius:12px;padding:16px 24px;
    box-shadow:0 2px 12px rgba(0,0,0,0.06);margin-bottom:32px;display:flex;align-items:center;gap:24px;flex-wrap:wrap;}
  .ji-item{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--slate);}
  .ji-val{font-weight:500;color:var(--charcoal);}
  .seat-layout{display:grid;grid-template-columns:1fr 1fr;gap:32px;}
  .seat-bus-frame{background:white;border-radius:20px;padding:24px;box-shadow:0 4px 24px rgba(0,0,0,0.1);}
  .bus-front{background:linear-gradient(135deg,var(--charcoal),var(--slate));border-radius:12px 12px 0 0;
    height:48px;display:flex;align-items:center;justify-content:center;color:white;font-size:12px;
    font-weight:500;margin-bottom:16px;letter-spacing:1px;}
  .seat-row{display:flex;justify-content:space-between;margin-bottom:10px;align-items:center;}
  .seat-row-num{font-size:11px;color:var(--muted);width:20px;}
  .seat-group{display:flex;gap:8px;}
  .seat{width:38px;height:38px;border-radius:8px 8px 4px 4px;display:flex;align-items:center;
    justify-content:center;font-size:11px;font-weight:600;cursor:pointer;border:2px solid transparent;
    transition:all .2s;position:relative;}
  .seat::after{content:'';position:absolute;bottom:-4px;left:4px;right:4px;height:4px;border-radius:0 0 4px 4px;}
  .seat.available{background:#E8F5E9;color:var(--green-mid);border-color:#A5D6A7;}
  .seat.available::after{background:#A5D6A7;}
  .seat.available:hover{background:#C8E6C9;transform:scale(1.1);}
  .seat.booked{background:#FFEBEE;color:#E57373;border-color:#FFCDD2;cursor:not-allowed;}
  .seat.booked::after{background:#FFCDD2;}
  .seat.selected{background:var(--saffron);color:white;border-color:#E65100;transform:scale(1.05);}
  .seat.selected::after{background:#E65100;}
  .aisle{width:24px;display:flex;align-items:center;justify-content:center;}
  .aisle-label{font-size:10px;color:var(--muted);writing-mode:vertical-lr;letter-spacing:2px;}
  .seat-legend{display:flex;gap:16px;margin-top:16px;justify-content:center;flex-wrap:wrap;}
  .legend-item{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--slate);}
  .legend-dot{width:14px;height:14px;border-radius:3px;}
  .seat-summary-card{background:white;border-radius:20px;padding:28px;
    box-shadow:0 4px 24px rgba(0,0,0,0.1);height:fit-content;position:sticky;top:80px;}
  .seat-summary-card h3{font-size:18px;margin-bottom:20px;}
  .summary-row{display:flex;justify-content:space-between;font-size:14px;margin-bottom:12px;color:var(--slate);}
  .summary-row.total{font-weight:600;color:var(--charcoal);font-size:16px;
    border-top:1px solid var(--border);padding-top:12px;margin-top:8px;}
  .no-seat-msg{text-align:center;color:var(--muted);font-size:14px;padding:20px 0;}
  .selected-seat-tag{display:inline-block;background:var(--saffron-pale);color:var(--saffron);
    border-radius:6px;padding:4px 10px;font-size:13px;font-weight:500;margin:3px;}
  .btn-proceed{width:100%;padding:14px;background:linear-gradient(135deg,var(--saffron),var(--saffron-light));
    color:white;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;
    font-family:'DM Sans';transition:all .2s;margin-top:20px;}
  .btn-proceed:hover{box-shadow:0 8px 24px rgba(255,107,0,0.4);}
  .btn-proceed:disabled{background:#DDD;cursor:not-allowed;box-shadow:none;}

  /* ── CONFIRM + FOOD ── */
  .confirm-page{max-width:800px;margin:0 auto;padding:48px 24px;}
  .confirm-page h2{font-size:32px;margin-bottom:8px;}
  .confirm-card{background:white;border-radius:20px;padding:32px;
    box-shadow:0 4px 24px rgba(0,0,0,0.08);margin-bottom:24px;}
  .confirm-card h3{font-size:18px;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--border);}
  .detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .detail-item label{font-size:12px;color:var(--muted);display:block;margin-bottom:4px;}
  .detail-item span{font-size:15px;font-weight:500;color:var(--charcoal);}
  .food-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px;margin-top:16px;}
  .food-card{border:2px solid var(--border);border-radius:14px;padding:16px;cursor:pointer;
    transition:all .2s;text-align:center;}
  .food-card:hover{border-color:var(--saffron);background:var(--saffron-pale);}
  .food-card.selected{border-color:var(--saffron);background:var(--saffron-pale);}
  .food-emoji{font-size:40px;display:block;margin-bottom:8px;}
  .food-name{font-size:14px;font-weight:500;color:var(--charcoal);}
  .food-price{font-size:13px;color:var(--saffron);margin-top:4px;}
  .food-qty{display:flex;align-items:center;gap:8px;justify-content:center;margin-top:10px;}
  .qty-btn{width:24px;height:24px;border-radius:6px;border:1.5px solid var(--border);background:white;
    cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;font-family:'DM Sans';}
  .qty-btn:hover{background:var(--saffron);color:white;border-color:var(--saffron);}
  .qty-val{font-size:14px;font-weight:500;min-width:20px;text-align:center;}

  /* ── PAYMENT ── */
  .payment-page{max-width:700px;margin:0 auto;padding:48px 24px;}
  .payment-page h2{font-size:32px;margin-bottom:8px;}
  .payment-card{background:white;border-radius:20px;padding:32px;
    box-shadow:0 4px 24px rgba(0,0,0,0.08);margin-bottom:24px;}
  .pay-methods{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap;}
  .pay-method{flex:1;min-width:100px;padding:14px;border:2px solid var(--border);border-radius:12px;
    text-align:center;cursor:pointer;transition:all .2s;}
  .pay-method.active{border-color:var(--saffron);background:var(--saffron-pale);}
  .pay-method .pm-icon{font-size:24px;display:block;margin-bottom:6px;}
  .pay-method .pm-name{font-size:13px;font-weight:500;color:var(--slate);}
  .card-form{display:none;}
  .card-form.active{display:block;}
  .card-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .price-breakdown{background:#F8F9FA;border-radius:12px;padding:20px;}
  .price-row{display:flex;justify-content:space-between;font-size:14px;margin-bottom:10px;color:var(--slate);}
  .price-row.grand{font-size:18px;font-weight:700;color:var(--charcoal);
    border-top:2px solid var(--border);padding-top:12px;margin-top:4px;}
  .btn-pay{width:100%;padding:16px;background:linear-gradient(135deg,var(--green-mid),var(--green-dark));
    color:white;border:none;border-radius:12px;font-size:17px;font-weight:600;cursor:pointer;
    font-family:'DM Sans';transition:all .2s;margin-top:24px;}
  .btn-pay:hover{box-shadow:0 8px 24px rgba(27,94,32,0.4);transform:translateY(-1px);}

  /* ── SUCCESS ── */
  .success-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;
    align-items:center;justify-content:center;z-index:1000;}
  .success-card{background:white;border-radius:24px;padding:48px 40px;text-align:center;
    max-width:400px;animation:popIn .4s ease;}
  @keyframes popIn{from{transform:scale(.8);opacity:0}to{transform:scale(1);opacity:1}}
  .success-icon{font-size:64px;display:block;margin-bottom:16px;}
  .success-card h2{font-size:28px;margin-bottom:12px;color:var(--success);}
  .success-card p{color:var(--slate);margin-bottom:24px;}
  .ticket-id{background:var(--green-light);border-radius:10px;padding:12px 20px;
    font-size:15px;font-weight:600;color:var(--green-dark);}

  /* ── ROUTES ── */
  .routes-page{max-width:900px;margin:0 auto;padding:48px 24px;}
  .routes-page h2{font-size:32px;margin-bottom:8px;}
  .route-form{background:white;border-radius:16px;padding:24px 28px;
    box-shadow:0 2px 12px rgba(0,0,0,0.06);margin-bottom:32px;display:flex;
    gap:16px;align-items:flex-end;flex-wrap:wrap;}
  .route-result{background:white;border-radius:20px;overflow:hidden;
    box-shadow:0 4px 24px rgba(0,0,0,0.08);animation:fadeUp .4s;}
  .route-header{background:linear-gradient(135deg,var(--charcoal),var(--slate));padding:24px 28px;color:white;}
  .route-header h3{font-size:22px;margin-bottom:4px;}
  .route-header p{opacity:.7;font-size:14px;}
  .stop-timeline{padding:28px;}
  .stop-item{display:flex;gap:16px;margin-bottom:24px;}
  .stop-item:last-child{margin-bottom:0;}
  .stop-indicator{display:flex;flex-direction:column;align-items:center;flex-shrink:0;width:40px;}
  .stop-dot{width:16px;height:16px;border-radius:50%;flex-shrink:0;border:3px solid var(--saffron);background:white;}
  .stop-dot.start{background:var(--saffron);}
  .stop-dot.end{background:var(--green-mid);border-color:var(--green-mid);}
  .stop-line{flex:1;width:2px;background:linear-gradient(180deg,var(--saffron),var(--green-mid));margin-top:4px;}
  .stop-content{flex:1;padding-bottom:8px;}
  .stop-name{font-size:16px;font-weight:600;color:var(--charcoal);}
  .stop-time{font-size:13px;color:var(--muted);margin-top:2px;}
  .stop-badge{display:inline-flex;align-items:center;gap:4px;background:#F5F5F5;border-radius:6px;
    padding:4px 10px;font-size:12px;color:var(--slate);margin-top:6px;}

  

  /* ── MY BOOKINGS ── */
  .mybookings-page{max-width:900px;margin:0 auto;padding:48px 24px;}
  .mybookings-page h2{font-size:32px;margin-bottom:8px;}
  .booking-ticket{background:white;border-radius:20px;overflow:hidden;
    box-shadow:0 4px 24px rgba(0,0,0,.08);margin-bottom:20px;display:flex;}
  .ticket-stripe{width:8px;background:linear-gradient(180deg,var(--saffron),var(--green-mid));}
  .ticket-body{flex:1;padding:24px 28px;}
  .ticket-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;}
  .ticket-route{font-size:20px;font-weight:600;color:var(--charcoal);}
  .ticket-id-small{font-size:12px;color:var(--muted);margin-top:2px;}
  .ticket-status{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;}
  .ticket-status.confirmed{background:var(--green-light);color:var(--green-dark);}
  .ticket-details{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;}
  .td-item label{font-size:11px;color:var(--muted);display:block;margin-bottom:3px;text-transform:uppercase;letter-spacing:.5px;}
  .td-item span{font-size:14px;font-weight:500;color:var(--charcoal);}
  .no-bookings{text-align:center;padding:60px 24px;color:var(--muted);}
  .no-bookings-icon{font-size:64px;display:block;margin-bottom:16px;}

  /* ── FOOTER ── */
  footer{background:var(--charcoal);color:white;padding:40px 24px 24px;margin-top:auto;}
  .footer-inner{max-width:1200px;margin:0 auto;}
  .footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;margin-bottom:32px;}
  .footer-col h4{font-size:14px;font-weight:600;margin-bottom:12px;opacity:.5;
    letter-spacing:1px;text-transform:uppercase;}
  .footer-col p,.footer-col a{font-size:13px;color:rgba(255,255,255,0.6);display:block;
    margin-bottom:6px;text-decoration:none;transition:color .2s;}
  .footer-col a:hover{color:var(--saffron);}
  .footer-bottom{border-top:1px solid rgba(255,255,255,0.08);padding-top:20px;
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;}
  .footer-bottom p{font-size:13px;color:rgba(255,255,255,0.4);}
  .back-btn{display:flex;align-items:center;gap:6px;font-size:14px;color:var(--slate);
    cursor:pointer;margin-bottom:24px;background:none;border:none;font-family:'DM Sans';padding:0;}
  .back-btn:hover{color:var(--saffron);}

  @media(max-width:700px){
    .input-row,.seat-layout,.tracking-layout,.detail-grid{grid-template-columns:1fr;}
    .hero-content h1{font-size:32px;}
    .ticket-details{grid-template-columns:1fr 1fr;}
  }
</style>
</head>
<body>

<!-- ════ AUTH ════ -->
<div id="auth-screen">
  <div class="auth-card">
    <div class="auth-logo">
      <div class="logo-icon">🚌</div>
      <h1>BUSZIN</h1>
      <p>Tamil Nadu's Premier Bus Network</p>
    </div>
    <div class="auth-tabs">
      <div class="auth-tab active" id="tab-login" onclick="switchTab('login')">Login</div>
      <div class="auth-tab" id="tab-signup" onclick="switchTab('signup')">Sign Up</div>
    </div>
    <div id="login-form">
      <div class="form-group"><label>Email Address</label><input type="email" id="login-email" placeholder="you@example.com"/></div>
      <div class="form-group"><label>Password</label><input type="password" id="login-password" placeholder="••••••••"/></div>
      <div class="auth-error" id="login-error"></div>
      <button class="btn-primary" style="margin-top:8px" onclick="doLogin()">Login →</button>
    </div>
    <div id="signup-form" style="display:none">
      <div class="form-group"><label>Full Name</label><input type="text" id="signup-name" placeholder="Your full name"/></div>
      <div class="form-group"><label>Email Address</label><input type="email" id="signup-email" placeholder="you@example.com"/></div>
      <div class="form-group"><label>Password</label><input type="password" id="signup-password" placeholder="Min 6 characters"/></div>
      <div class="auth-error" id="signup-error"></div>
      <button class="btn-primary" style="margin-top:8px" onclick="doSignup()">Create Account →</button>
    </div>
  </div>
</div>

<!-- ════ APP ════ -->
<div id="app">
  <nav class="navbar">
    <div class="nav-inner">
      <div class="nav-logo"><span>🚌</span> BUSZIN</div>
      <button class="nav-btn active" id="nav-home"     onclick="showPage('home')">Home</button>
      <button class="nav-btn"        id="nav-book"     onclick="showPage('book')">Book Bus</button>
      <button class="nav-btn"        id="nav-routes"   onclick="showPage('routes')">Bus Routes</button>
      
      <button class="nav-btn"        id="nav-mybookings" onclick="showPage('mybookings')">My Bookings</button>
      <div class="nav-user">
        <div class="nav-avatar" id="nav-avatar">U</div>
        <span class="nav-user-name" id="nav-username">User</span>
        <button class="btn-logout" onclick="logout()">Logout</button>
      </div>
    </div>
  </nav>

  <!-- HOME -->
  <div class="page active" id="page-home">
    <div class="hero">
      <div class="hero-bg"></div>
      <div class="hero-pattern"></div>
      <div class="hero-content">
        
        <p>Safe, comfortable &amp; punctual bus travel across the state</p>
        <br><br>
        <button class="btn-primary" style="width:auto;padding:14px 40px;margin-top:8px" onclick="showPage('book')">Book Your Journey →</button>
      </div>
    </div>
    
  </div>

  <!-- BOOK BUS -->
  <div class="page" id="page-book">
    <div class="booking-page">
      <h2>Book Your Bus</h2>
      <p class="sub">Find and book buses across Tamil Nadu</p>
      <div class="booking-form-card">
        <div class="input-row">
          <div class="field-wrap">
            <label class="field-label">🚉 From</label>
            <input class="field-input" id="inp-from" placeholder="Enter source city..." autocomplete="off"
              oninput="autocomplete('from',this.value)" onfocus="autocomplete('from',this.value)"/>
            <div class="autocomplete-list" id="ac-from"></div>
          </div>
          <div class="field-wrap">
            <label class="field-label">🏁 To</label>
            <input class="field-input" id="inp-to" placeholder="Enter destination..." autocomplete="off"
              oninput="autocomplete('to',this.value)" onfocus="autocomplete('to',this.value)"/>
            <div class="autocomplete-list" id="ac-to"></div>
          </div>
          <div class="field-wrap">
            <label class="field-label">📅 Date of Travel</label>
            <input class="field-input" type="date" id="inp-date"/>
          </div>
        </div>
        <div style="margin-top:20px;text-align:right">
          <button class="btn-search" onclick="searchBuses()">🔍 Search Buses</button>
        </div>
      </div>
      <div id="bus-results"></div>
    </div>
  </div>

  <!-- SEATS -->
  <div class="page" id="page-seats">
    <div class="seat-page">
      <button class="back-btn" onclick="showPage('book')">← Back to results</button>
      <h2>Select Your Seat</h2>
      <p style="color:var(--muted);margin-bottom:24px;font-size:14px">Click on available seats to select</p>
      <div class="journey-info-bar" id="seat-journey-bar"></div>
      <div class="seat-layout">
        <div>
          <div class="seat-bus-frame">
            <div class="bus-front">🚌 DRIVER + ENGINE</div>
            <div id="seat-grid"></div>
            <div class="seat-legend">
              <div class="legend-item"><div class="legend-dot" style="background:#E8F5E9;border:2px solid #A5D6A7"></div> Available</div>
              <div class="legend-item"><div class="legend-dot" style="background:#FFEBEE;border:2px solid #FFCDD2"></div> Booked</div>
              <div class="legend-item"><div class="legend-dot" style="background:var(--saffron);border:2px solid #E65100"></div> Your seat</div>
            </div>
          </div>
        </div>
        <div>
          <div class="seat-summary-card">
            <h3>Booking Summary</h3>
            <div class="summary-row"><span>Route</span><span id="sum-route" style="font-weight:500">—</span></div>
            <div class="summary-row"><span>Date</span><span id="sum-date" style="font-weight:500">—</span></div>
            <div class="summary-row"><span>Departure</span><span id="sum-depart" style="font-weight:500">—</span></div>
            <div class="summary-row"><span>Bus</span><span id="sum-bus" style="font-weight:500">—</span></div>
            <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--border)">
              <div style="font-size:13px;color:var(--muted);margin-bottom:8px">Selected Seats</div>
              <div id="selected-seats-tags"><div class="no-seat-msg">No seats selected</div></div>
            </div>
            <div class="summary-row total" style="margin-top:16px"><span>Total</span><span id="sum-total">₹0</span></div>
            <button class="btn-proceed" onclick="proceedToConfirm()" id="btn-proceed-seats" disabled>Proceed to Confirm →</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- CONFIRM + FOOD -->
  <div class="page" id="page-confirm">
    <div class="confirm-page">
      <button class="back-btn" onclick="showPage('seats')">← Back to seats</button>
      <h2>Confirm Booking</h2>
      <p style="color:var(--muted);margin-bottom:28px;font-size:14px">Review your journey details</p>
      <div class="confirm-card">
        <h3>Journey Details</h3>
        <div class="detail-grid" id="journey-details-grid"></div>
      </div>
      <div class="confirm-card">
        <h3>🍱 Add Food During Journey</h3>
        <p style="font-size:14px;color:var(--muted);margin-bottom:4px">Enjoy freshly prepared meals during your trip (optional)</p>
        <div class="food-grid" id="food-grid"></div>
      </div>
      <div style="display:flex;justify-content:flex-end">
        <button class="btn-proceed" style="max-width:260px" onclick="goToPayment()">Continue to Payment →</button>
      </div>
    </div>
  </div>

  <!-- PAYMENT -->
  <div class="page" id="page-payment">
    <div class="payment-page">
      <button class="back-btn" onclick="showPage('confirm')">← Back</button>
      <h2>Payment</h2>
      <p style="color:var(--muted);margin-bottom:28px;font-size:14px">Complete your booking securely</p>
      <div class="payment-card">
        <h3 style="font-size:18px;margin-bottom:20px">Choose Payment Method</h3>
        <div class="pay-methods">
          <div class="pay-method active" onclick="selectPayMethod('card',this)"><span class="pm-icon">💳</span><span class="pm-name">Card</span></div>
          <div class="pay-method" onclick="selectPayMethod('upi',this)"><span class="pm-icon">📱</span><span class="pm-name">UPI</span></div>
          <div class="pay-method" onclick="selectPayMethod('netbanking',this)"><span class="pm-icon">🏦</span><span class="pm-name">Net Banking</span></div>
          <div class="pay-method" onclick="selectPayMethod('wallet',this)"><span class="pm-icon">👛</span><span class="pm-name">Wallet</span></div>
        </div>
        <div class="card-form active" id="pay-card">
          <div class="form-group"><label class="field-label">Card Number</label><input class="field-input" placeholder="1234  5678  9012  3456" maxlength="19" oninput="formatCard(this)"/></div>
          <div class="card-row">
            <div class="form-group"><label class="field-label">Expiry</label><input class="field-input" placeholder="MM/YY" maxlength="5"/></div>
            <div class="form-group"><label class="field-label">CVV</label><input class="field-input" placeholder="•••" maxlength="3" type="password"/></div>
          </div>
          <div class="form-group"><label class="field-label">Name on Card</label><input class="field-input" placeholder="As on card"/></div>
        </div>
        <div class="card-form" id="pay-upi">
          <div class="form-group"><label class="field-label">UPI ID</label><input class="field-input" placeholder="yourname@upi"/></div>
        </div>
        <div class="card-form" id="pay-netbanking">
          <div class="form-group"><label class="field-label">Select Bank</label>
          <select class="field-input"><option>State Bank of India</option><option>HDFC Bank</option><option>ICICI Bank</option><option>Axis Bank</option><option>Indian Bank</option><option>Canara Bank</option></select></div>
        </div>
        <div class="card-form" id="pay-wallet">
          <div class="form-group"><label class="field-label">Select Wallet</label>
          <select class="field-input"><option>Paytm</option><option>PhonePe</option><option>Google Pay</option><option>Amazon Pay</option></select></div>
        </div>
      </div>
      <div class="payment-card">
        <h3 style="font-size:18px;margin-bottom:16px">Price Breakdown</h3>
        <div class="price-breakdown" id="price-breakdown"></div>
        <button class="btn-pay" onclick="processPayment()">🔒 Pay Now</button>
      </div>
    </div>
  </div>

  <!-- ROUTES -->
  <div class="page" id="page-routes">
    <div class="routes-page">
      <h2>Bus Routes</h2>
      <p style="color:var(--muted);margin-bottom:28px;font-size:14px">Explore complete routes with stop details and timings</p>
      <div class="route-form">
        <div class="field-wrap" style="flex:1;min-width:160px">
          <label class="field-label">From</label>
          <input class="field-input" id="route-from" placeholder="Source city..." autocomplete="off"
            oninput="autocomplete('rfrom',this.value)" onfocus="autocomplete('rfrom',this.value)"/>
          <div class="autocomplete-list" id="ac-rfrom"></div>
        </div>
        <div class="field-wrap" style="flex:1;min-width:160px">
          <label class="field-label">To</label>
          <input class="field-input" id="route-to" placeholder="Destination..." autocomplete="off"
            oninput="autocomplete('rto',this.value)" onfocus="autocomplete('rto',this.value)"/>
          <div class="autocomplete-list" id="ac-rto"></div>
        </div>
        <button class="btn-search" onclick="showRoute()">Show Route</button>
      </div>
      <div id="route-result"></div>
    </div>
  </div>

  

  <!-- MY BOOKINGS -->
  <div class="page" id="page-mybookings">
    <div class="mybookings-page">
      <h2>My Bookings</h2>
      <p style="color:var(--muted);margin-bottom:32px;font-size:14px">All your past and upcoming tickets</p>
      <div id="mybookings-list"></div>
    </div>
  </div>

  <footer>
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-col">
          <div style="font-family:'Playfair Display';font-size:20px;margin-bottom:8px">🚌 BUSZIN</div>
          <p>Tamil Nadu's most reliable bus booking platform, serving millions of passengers across the state.</p>
        </div>
        <div class="footer-col">
          <h4>Quick Links</h4>
          <a href="#" onclick="showPage('book')">Book Tickets</a>
          <a href="#" onclick="showPage('routes')">Bus Routes</a>
          
          <a href="#" onclick="showPage('mybookings')">My Bookings</a>
        </div>
        <div class="footer-col">
          <h4>Support</h4>
          <a href="#">Help Center</a><a href="#">Cancellation Policy</a>
          <a href="#">Refund Status</a><a href="#">Contact Us</a>
        </div>
        <div class="footer-col">
          <h4>Popular Routes</h4>
          <a href="#">Chennai → Madurai</a><a href="#">Chennai → Coimbatore</a>
          <a href="#">Chennai → Trichy</a><a href="#">Chennai → Salem</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2025 BUSZIN Bus Services. All rights reserved. | A Government of Tamil Nadu Initiative.</p>
        <p style="color:rgba(255,255,255,0.3)">Made with ❤️ in Chennai</p>
      </div>
    </div>
  </footer>
</div>

<!-- SUCCESS OVERLAY -->
<div class="success-overlay" id="success-overlay" style="display:none;align-items:center;justify-content:center">
  <div class="success-card">
    <span class="success-icon">🎉</span>
    <h2>Booking Confirmed!</h2>
    <p>Your bus ticket has been booked successfully. Have a safe journey!</p>
    <div class="ticket-id" id="ticket-id-display">Ticket #TN-000000</div>
    <button class="btn-primary" style="margin-top:24px"
      onclick="document.getElementById('success-overlay').style.display='none';saveBooking();showPage('mybookings')">View My Bookings</button>
  </div>
</div>

<script>
// ── DATA ──
const TN_CITIES=['Chennai','Madurai','Coimbatore','Trichy','Salem','Tirunelveli','Vellore','Erode',
  'Tiruppur','Thoothukudi','Dindigul','Thanjavur','Kanchipuram','Cuddalore','Karur','Nagercoil',
  'Namakkal','Villupuram','Puducherry','Hosur','Ooty','Kodaikanal','Kumbakonam','Chidambaram',
  'Nagapattinam','Ramanathapuram','Virudhunagar','Sivakasi','Pollachi','Mettupalayam',
  'Ambattur','Tiruvallur','Mahabalipuram','Krishnagiri','Dharmapuri','Perambalur','Ariyalur',
  'Kallakurichi','Ranipet','Tirupattur','Tenkasi'];

const TRAVEL_COMPANIES=[
  {name:'TNSTC Express',type:'State Express',color:'#1B5E20',bg:'#E8F5E9',emoji:'🟢'},
  {name:'Parveen Travels',type:'AC Sleeper',color:'#1565C0',bg:'#E3F2FD',emoji:'🔵'},
  {name:'KPN Travels',type:'Volvo AC',color:'#4A148C',bg:'#F3E5F5',emoji:'🟣'},
  {name:'SRS Travels',type:'Non-AC Sleeper',color:'#E65100',bg:'#FFF3E0',emoji:'🟠'},
  {name:'VRL Travels',type:'Multi-Axle Sleeper',color:'#880E4F',bg:'#FCE4EC',emoji:'🔴'},
  {name:'Orange Tours',type:'AC Chair Car',color:'#F57F17',bg:'#FFFDE7',emoji:'🟡'}
];



const FOODS=[
  {name:'Biryani',emoji:'🍛',price:150},{name:'Idli Sambar',emoji:'🥘',price:80},
  {name:'Meals Thali',emoji:'🍽️',price:120},{name:'Chicken Curry',emoji:'🍗',price:180},
  {name:'Veg Sandwich',emoji:'🥪',price:70},{name:'Filter Coffee',emoji:'☕',price:40},
  {name:'Samosa',emoji:'🥟',price:50},{name:'Pongal',emoji:'🫕',price:90}
];



const ROUTE_STOPS={
  'Chennai-Madurai':[{name:'Chennai Central',time:'06:00',dist:'0 km'},{name:'Tambaram',time:'06:35',dist:'27 km'},{name:'Chengalpattu',time:'07:10',dist:'57 km'},{name:'Tindivanam',time:'08:00',dist:'104 km'},{name:'Villupuram',time:'08:45',dist:'162 km'},{name:'Trichy',time:'10:30',dist:'327 km'},{name:'Dindigul',time:'11:30',dist:'398 km'},{name:'Madurai',time:'12:30',dist:'461 km'}],
  'Chennai-Coimbatore':[{name:'Chennai Central',time:'07:00',dist:'0 km'},{name:'Kanchipuram',time:'07:50',dist:'72 km'},{name:'Vellore',time:'09:00',dist:'140 km'},{name:'Salem',time:'11:00',dist:'290 km'},{name:'Erode',time:'12:15',dist:'370 km'},{name:'Tiruppur',time:'13:00',dist:'424 km'},{name:'Coimbatore',time:'13:45',dist:'497 km'}],
  'Chennai-Trichy':[{name:'Chennai Central',time:'08:00',dist:'0 km'},{name:'Tambaram',time:'08:40',dist:'27 km'},{name:'Villupuram',time:'10:30',dist:'162 km'},{name:'Cuddalore',time:'11:10',dist:'195 km'},{name:'Chidambaram',time:'12:00',dist:'229 km'},{name:'Kumbakonam',time:'13:30',dist:'295 km'},{name:'Trichy',time:'14:30',dist:'327 km'}]
};

// ── STATE ──
let users=JSON.parse(localStorage.getItem('buszin_users')||'[]');
let currentUser=JSON.parse(localStorage.getItem('buszin_current')||'null');
let savedBookings=JSON.parse(localStorage.getItem('buszin_bookings')||'[]');
let booking={from:'',to:'',date:'',bus:null,seats:[],fare:0};
let foodOrders={};
let currentTicketId='';
let busPositions={};
let selectedTrackBus=null;
let trackInterval=null;

// ── AUTH ──
function switchTab(tab){
  document.getElementById('tab-login').classList.toggle('active',tab==='login');
  document.getElementById('tab-signup').classList.toggle('active',tab==='signup');
  document.getElementById('login-form').style.display=tab==='login'?'block':'none';
  document.getElementById('signup-form').style.display=tab==='signup'?'block':'none';
}
function doLogin(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-password').value;
  const user=users.find(u=>u.email===email&&u.password===pass);
  if(!user){document.getElementById('login-error').textContent='Invalid email or password.';return;}
  document.getElementById('login-error').textContent='';
  loginUser(user);
}
function doSignup(){
  const name=document.getElementById('signup-name').value.trim();
  const email=document.getElementById('signup-email').value.trim();
  const pass=document.getElementById('signup-password').value;
  if(!name||!email||!pass){document.getElementById('signup-error').textContent='All fields required.';return;}
  if(pass.length<6){document.getElementById('signup-error').textContent='Password must be at least 6 characters.';return;}
  if(users.find(u=>u.email===email)){document.getElementById('signup-error').textContent='Email already registered.';return;}
  const user={name,email,password:pass,id:Date.now()};
  users.push(user);
  localStorage.setItem('buszin_users',JSON.stringify(users));
  loginUser(user);
}
function loginUser(user){
  currentUser=user;
  localStorage.setItem('buszin_current',JSON.stringify(user));
  document.getElementById('auth-screen').style.display='none';
  document.getElementById('app').style.display='flex';
  document.getElementById('nav-username').textContent=user.name.split(' ')[0];
  document.getElementById('nav-avatar').textContent=user.name.charAt(0).toUpperCase();
  initApp();
}
function logout(){
  currentUser=null;
  localStorage.removeItem('buszin_current');
  document.getElementById('app').style.display='none';
  document.getElementById('auth-screen').style.display='flex';
  
}

// ── INIT ──
function initApp(){
  const today=new Date().toISOString().split('T')[0];
  document.getElementById('inp-date').min=today;
  document.getElementById('inp-date').value=today;
  
  
  showPage('home');
}

// ── PAGES ──
function showPage(name){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('page-'+name).classList.add('active');
  const nb=document.getElementById('nav-'+name);
  if(nb)nb.classList.add('active');
  window.scrollTo(0,0);
  
  if(name==='mybookings')renderMyBookings();
}

// ── AUTOCOMPLETE ──
const AC_MAP={from:'inp-from',to:'inp-to',rfrom:'route-from',rto:'route-to'};
const AC_LIST={from:'ac-from',to:'ac-to',rfrom:'ac-rfrom',rto:'ac-rto'};
function autocomplete(field,val){
  const list=document.getElementById(AC_LIST[field]);
  if(!val.trim()){list.style.display='none';return;}
  const matches=TN_CITIES.filter(c=>c.toLowerCase().includes(val.toLowerCase())).slice(0,8);
  if(!matches.length){list.style.display='none';return;}
  list.innerHTML=matches.map(c=>`<div class="autocomplete-item" onclick="selectCity('${field}','${c}')"><span>📍</span>${c}</div>`).join('');
  list.style.display='block';
}
function selectCity(field,city){
  document.getElementById(AC_MAP[field]).value=city;
  document.getElementById(AC_LIST[field]).style.display='none';
  if(field==='from')booking.from=city;
  if(field==='to')booking.to=city;
}
document.addEventListener('click',e=>{if(!e.target.closest('.field-wrap'))document.querySelectorAll('.autocomplete-list').forEach(l=>l.style.display='none');});

// ── SEARCH ──
function searchBuses(){
  booking.from=document.getElementById('inp-from').value.trim();
  booking.to=document.getElementById('inp-to').value.trim();
  booking.date=document.getElementById('inp-date').value;
  if(!booking.from||!booking.to||!booking.date){alert('Please fill in all fields.');return;}
  if(booking.from===booking.to){alert('Source and destination cannot be the same!');return;}
  const container=document.getElementById('bus-results');
  container.innerHTML=`<div style="text-align:center;padding:40px;color:var(--muted)"><div style="font-size:40px">🔍</div><p style="margin-top:12px">Finding best buses for you...</p></div>`;
  setTimeout(()=>{renderBuses(generateBuses(),container);},800);
}
function generateBuses(){
  const hrs=Math.floor(Math.random()*4)+2;
  const timings=['06:00','07:30','09:00','10:30','13:00','15:30','18:00','20:00','22:30'];
  return timings.slice(0,Math.floor(Math.random()*4)+4).map((dep,i)=>{
    const c=TRAVEL_COMPANIES[i%TRAVEL_COMPANIES.length];
    const[h,m]=dep.split(':').map(Number);
    const am=(h*60+m)+hrs*60+Math.floor(Math.random()*30);
    const arr=`${String(Math.floor(am/60)%24).padStart(2,'0')}:${String(am%60).padStart(2,'0')}`;
    const fare=200+hrs*40+Math.floor(Math.random()*100);
    const seats=Math.floor(Math.random()*20)+5;
    const amenities=['WiFi','AC','Charging','Water','Blanket','Snacks'].filter(()=>Math.random()>.5);
    return{id:i,company:c,dep,arr,duration:`${hrs}h ${Math.floor(Math.random()*30)+10}m`,fare,seats,amenities};
  });
}
function renderBuses(buses,container){
  const dateDisplay=new Date(booking.date).toLocaleDateString('en-IN',{weekday:'long',day:'numeric',month:'long'});
  container.innerHTML=`<div class="results-section">
    <div class="results-header"><div><h3>${booking.from} → ${booking.to}</h3><p style="color:var(--muted);font-size:14px;margin-top:4px">${dateDisplay}</p></div>
    <div class="results-count">${buses.length} buses found</div></div>
    ${buses.map(b=>`<div class="bus-card">
      <div class="bus-logo" style="background:${b.company.bg};color:${b.company.color}">${b.company.emoji}🚌</div>
      <div class="bus-info">
        <div class="bus-name">${b.company.name}</div>
        <div class="bus-type">${b.company.type}</div>
        <div class="bus-amenities">${b.amenities.map(a=>`<span class="amenity">${a}</span>`).join('')}</div>
        <div class="bus-times">
          <div class="time-block"><div class="time-big">${b.dep}</div><div class="time-label">${booking.from}</div></div>
          <div class="duration-line"><div class="dur-line"></div><div class="dur-text">${b.duration}</div></div>
          <div class="time-block"><div class="time-big">${b.arr}</div><div class="time-label">${booking.to}</div></div>
        </div>
      </div>
      <div class="bus-fare"><div class="fare-price">₹${b.fare}</div><div class="fare-label">per seat</div><div class="fare-seats">🟢 ${b.seats} seats left</div></div>
      <button class="btn-book" onclick='selectBus(${JSON.stringify(b)})'>Book Now</button>
    </div>`).join('')}
  </div>`;
}

// ── SEATS ──
function selectBus(bus){booking.bus=bus;booking.seats=[];renderSeatPage();showPage('seats');}
function renderSeatPage(){
  const b=booking.bus;
  document.getElementById('seat-journey-bar').innerHTML=
    `<div class="ji-item">🚉 <span class="ji-val">${booking.from}</span></div>
    <div class="ji-item">→</div>
    <div class="ji-item">🏁 <span class="ji-val">${booking.to}</span></div>
    <div class="ji-item">📅 <span class="ji-val">${new Date(booking.date).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})}</span></div>
    <div class="ji-item">🕐 <span class="ji-val">${b.dep} → ${b.arr}</span></div>
    <div class="ji-item">🚌 <span class="ji-val">${b.company.name}</span></div>`;
  document.getElementById('sum-route').textContent=`${booking.from} → ${booking.to}`;
  document.getElementById('sum-date').textContent=new Date(booking.date).toLocaleDateString('en-IN');
  document.getElementById('sum-depart').textContent=b.dep;
  document.getElementById('sum-bus').textContent=b.company.name;
  const bookedSeats=new Set();
  while(bookedSeats.size<Math.floor(Math.random()*15)+5)bookedSeats.add(Math.floor(Math.random()*40)+1);
  let html='';
  for(let row=1;row<=10;row++){
    const s=[row*4-3,row*4-2,row*4-1,row*4];
    html+=`<div class="seat-row"><div class="seat-row-num">${row}</div>
      <div class="seat-group">${[s[0],s[1]].map(n=>`<div class="seat ${bookedSeats.has(n)?'booked':'available'}" id="seat-${n}" onclick="toggleSeat(${n},${bookedSeats.has(n)},${b.fare})">${n}</div>`).join('')}</div>
      <div class="aisle"><div class="aisle-label">AISLE</div></div>
      <div class="seat-group">${[s[2],s[3]].map(n=>`<div class="seat ${bookedSeats.has(n)?'booked':'available'}" id="seat-${n}" onclick="toggleSeat(${n},${bookedSeats.has(n)},${b.fare})">${n}</div>`).join('')}</div>
    </div>`;
  }
  document.getElementById('seat-grid').innerHTML=html;
  updateSeatSummary();
}
function toggleSeat(num,isBooked,fare){
  if(isBooked)return;
  const el=document.getElementById('seat-'+num);
  const idx=booking.seats.indexOf(num);
  if(idx>-1){booking.seats.splice(idx,1);el.classList.remove('selected');el.classList.add('available');}
  else{booking.seats.push(num);el.classList.remove('available');el.classList.add('selected');}
  updateSeatSummary();
}
function updateSeatSummary(){
  const total=booking.seats.length*booking.bus.fare;
  booking.fare=total;
  const tags=document.getElementById('selected-seats-tags');
  tags.innerHTML=booking.seats.length?booking.seats.map(s=>`<span class="selected-seat-tag">Seat ${s}</span>`).join(''):'<div class="no-seat-msg">No seats selected</div>';
  document.getElementById('sum-total').textContent=`₹${total}`;
  document.getElementById('btn-proceed-seats').disabled=!booking.seats.length;
}
function proceedToConfirm(){if(!booking.seats.length)return;renderConfirmPage();showPage('confirm');}

// ── CONFIRM ──
function renderConfirmPage(){
  const b=booking.bus; foodOrders={};
  document.getElementById('journey-details-grid').innerHTML=
    `<div class="detail-item"><label>Passenger Name</label><span>${currentUser.name}</span></div>
    <div class="detail-item"><label>Email</label><span>${currentUser.email}</span></div>
    <div class="detail-item"><label>From</label><span>${booking.from}</span></div>
    <div class="detail-item"><label>To</label><span>${booking.to}</span></div>
    <div class="detail-item"><label>Date of Travel</label><span>${new Date(booking.date).toLocaleDateString('en-IN',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}</span></div>
    <div class="detail-item"><label>Departure Time</label><span>${b.dep}</span></div>
    <div class="detail-item"><label>Seats Selected</label><span>${booking.seats.map(s=>'Seat '+s).join(', ')}</span></div>
    <div class="detail-item"><label>Travels Partner</label><span>${b.company.name} (${b.company.type})</span></div>`;
  document.getElementById('food-grid').innerHTML=FOODS.map((f,i)=>
    `<div class="food-card" id="food-card-${i}">
      <span class="food-emoji">${f.emoji}</span>
      <div class="food-name">${f.name}</div>
      <div class="food-price">₹${f.price}</div>
      <div class="food-qty">
        <button class="qty-btn" onclick="adjustFood(${i},${f.price},-1)">−</button>
        <span class="qty-val" id="food-qty-${i}">0</span>
        <button class="qty-btn" onclick="adjustFood(${i},${f.price},1)">+</button>
      </div>
    </div>`
  ).join('');
}
function adjustFood(idx,price,delta){
  if(!foodOrders[idx])foodOrders[idx]={qty:0,price,name:FOODS[idx].name,emoji:FOODS[idx].emoji};
  foodOrders[idx].qty=Math.max(0,foodOrders[idx].qty+delta);
  document.getElementById('food-qty-'+idx).textContent=foodOrders[idx].qty;
  document.getElementById('food-card-'+idx).classList.toggle('selected',foodOrders[idx].qty>0);
}
function goToPayment(){renderPaymentPage();showPage('payment');}

// ── PAYMENT ──
function renderPaymentPage(){
  const foodTotal=Object.values(foodOrders).reduce((s,f)=>s+f.qty*f.price,0);
  const tax=Math.round(booking.fare*0.05);
  const grand=booking.fare+foodTotal+tax;
  const foodLines=Object.values(foodOrders).filter(f=>f.qty>0)
    .map(f=>`<div class="price-row"><span>${f.emoji} ${f.name} × ${f.qty}</span><span>₹${f.qty*f.price}</span></div>`).join('');
  document.getElementById('price-breakdown').innerHTML=
    `<div class="price-row"><span>Bus Fare (${booking.seats.length} seat${booking.seats.length>1?'s':''})</span><span>₹${booking.fare}</span></div>
    ${foodLines}
    <div class="price-row"><span>GST (5%)</span><span>₹${tax}</span></div>
    <div class="price-row" style="color:var(--success)"><span>Convenience Fee</span><span>FREE</span></div>
    <div class="price-row grand"><span>Total Amount</span><span>₹${grand}</span></div>`;
}
function selectPayMethod(method,el){
  document.querySelectorAll('.pay-method').forEach(m=>m.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.card-form').forEach(f=>f.classList.remove('active'));
  document.getElementById('pay-'+method).classList.add('active');
}
function formatCard(inp){inp.value=inp.value.replace(/\D/g,'').replace(/(.{4})/g,'$1  ').trim().slice(0,22);}
function processPayment(){
  currentTicketId='TN-'+Math.random().toString(36).substr(2,8).toUpperCase();
  document.getElementById('ticket-id-display').textContent='Ticket #'+currentTicketId;
  const o=document.getElementById('success-overlay');
  o.style.display='flex';
}
function saveBooking(){
  const foodTotal=Object.values(foodOrders).reduce((s,f)=>s+f.qty*f.price,0);
  const tax=Math.round(booking.fare*0.05);
  const grand=booking.fare+foodTotal+tax;
  savedBookings.push({
    id:currentTicketId,
    userId:currentUser.id,
    from:booking.from,to:booking.to,date:booking.date,
    seats:booking.seats.slice(),
    busName:booking.bus.company.name,busType:booking.bus.company.type,
    dep:booking.bus.dep,arr:booking.bus.arr,
    fare:grand,bookedAt:new Date().toISOString()
  });
  localStorage.setItem('buszin_bookings',JSON.stringify(savedBookings));
}

// ── MY BOOKINGS ──
function renderMyBookings(){
  const myB=savedBookings.filter(b=>b.userId===currentUser.id);
  const el=document.getElementById('mybookings-list');
  if(!myB.length){
    el.innerHTML=`<div class="no-bookings"><span class="no-bookings-icon">🎫</span>
      <h3 style="font-size:22px;margin-bottom:8px">No bookings yet</h3>
      <p>Your confirmed tickets will appear here</p>
      <button class="btn-primary" style="width:auto;padding:12px 32px;margin-top:20px" onclick="showPage('book')">Book Your First Trip</button>
    </div>`;
    return;
  }
  el.innerHTML=[...myB].reverse().map(b=>
    `<div class="booking-ticket">
      <div class="ticket-stripe"></div>
      <div class="ticket-body">
        <div class="ticket-header">
          <div><div class="ticket-route">${b.from} → ${b.to}</div><div class="ticket-id-small"># ${b.id}</div></div>
          <div class="ticket-status confirmed">✓ Confirmed</div>
        </div>
        <div class="ticket-details">
          <div class="td-item"><label>Date</label><span>${new Date(b.date).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})}</span></div>
          <div class="td-item"><label>Departure</label><span>${b.dep} → ${b.arr}</span></div>
          <div class="td-item"><label>Seats</label><span>${b.seats.map(s=>'S'+s).join(', ')}</span></div>
          <div class="td-item"><label>Amount Paid</label><span style="color:var(--saffron);font-weight:700">₹${b.fare}</span></div>
        </div>
        <div style="margin-top:12px;font-size:13px;color:var(--muted)">🚌 ${b.busName} · ${b.busType}</div>
      </div>
    </div>`
  ).join('');
}

// ── ROUTES ──
function showRoute(){
  const from=document.getElementById('route-from').value.trim();
  const to=document.getElementById('route-to').value.trim();
  if(!from||!to){alert('Please enter source and destination');return;}
  const key=`${from}-${to}`;const altKey=`${to}-${from}`;
  let stops=ROUTE_STOPS[key]||ROUTE_STOPS[altKey];
  if(!stops){
    const n=Math.floor(Math.random()*4)+4;
    stops=[{name:from,time:'06:00',dist:'0 km'}];
    for(let i=1;i<n-1;i++){
      const city=TN_CITIES[Math.floor(Math.random()*TN_CITIES.length)];
      stops.push({name:city,time:`${String(6+Math.floor(i*(6/n))).padStart(2,'0')}:${String(Math.floor(Math.random()*30)).padStart(2,'0')}`,dist:`${i*50+Math.floor(Math.random()*30)} km`});
    }
    stops.push({name:to,time:`${6+n}:${String(Math.floor(Math.random()*30)).padStart(2,'0')}`,dist:`${n*50+Math.floor(Math.random()*40)} km`});
  }
  const totalDist=stops[stops.length-1].dist;
  const[h1,m1]=stops[0].time.split(':').map(Number);
  const[h2,m2]=stops[stops.length-1].time.split(':').map(Number);
  const diff=(h2*60+m2)-(h1*60+m1);
  const dur=`${Math.floor(diff/60)}h ${diff%60}m`;
  document.getElementById('route-result').innerHTML=
    `<div class="route-result">
      <div class="route-header"><h3>${stops[0].name} → ${stops[stops.length-1].name}</h3><p>${stops.length} stops · ${totalDist} total distance · Approx ${dur}</p></div>
      <div class="stop-timeline">${stops.map((s,i)=>
        `<div class="stop-item">
          <div class="stop-indicator"><div class="stop-dot ${i===0?'start':i===stops.length-1?'end':''}"></div>${i<stops.length-1?'<div class="stop-line"></div>':''}</div>
          <div class="stop-content"><div class="stop-name">${s.name}</div><div class="stop-time">🕐 ${s.time}</div>
          ${i>0?`<span class="stop-badge">📍 ${s.dist} from ${stops[0].name}</span>`:'<span class="stop-badge">🚉 Origin</span>'}
          </div>
        </div>`
      ).join('')}</div>
    </div>`;
}


// ── RESTORE SESSION ──
window.addEventListener('load',()=>{
  if(currentUser){
    document.getElementById('auth-screen').style.display='none';
    document.getElementById('app').style.display='flex';
    document.getElementById('nav-username').textContent=currentUser.name.split(' ')[0];
    document.getElementById('nav-avatar').textContent=currentUser.name.charAt(0).toUpperCase();
    initApp();
  } else if(users.length===0){switchTab('signup');}
});
</script>
</body>
</html>"""

# ─────────────────────── HTTP SERVER (serves the HTML app) ───────────────────
_html_content = HTML_APP.encode("utf-8")

class BuszinHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/images/"):
            try:
                file_path = self.path.lstrip("/")

                with open(file_path, "rb") as f:
                    data = f.read()   # ✅ read INSIDE

                self.send_response(200)

                if file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                    self.send_header("Content-Type", "image/jpeg")
                elif file_path.endswith(".png"):
                    self.send_header("Content-Type", "image/png")

                self.end_headers()
                self.wfile.write(data)   # ✅ use stored data

            except FileNotFoundError:
                self.send_error(404, "Image not found")

        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(_html_content)
    def log_message(self, *_):
        pass  # suppress server logs

def find_free_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def start_server(port):
    HTTPServer(("0.0.0.0", port), BuszinHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server

# ─────────────────────────── TKINTER LAUNCHER UI ─────────────────────────────
class BuszinLauncher:
    # ── colour palette (matches the app)
    SAFFRON     = "#FF6B00"
    GREEN_DARK  = "#1B5E20"
    GREEN_MID   = "#2E7D32"
    CREAM       = "#FAFAF7"
    CHARCOAL    = "#1A1A2E"
    SLATE       = "#4A4A6A"
    WHITE       = "#FFFFFF"
    MUTED       = "#8A8AA0"

    def __init__(self):
        self.port   = find_free_port()
        self.server = None
        self.url    = f"http://127.0.0.1:{self.port}"
        self._build_window()

    # ── window ───────────────────────────────────────────────────────────────
    def _build_window(self):
        self.root = tk.Tk()
        self.root.title("BUSZIN — Tamil Nadu Bus Booking")
        self.root.resizable(False, False)
        self.root.configure(bg=self.CHARCOAL)

        # Centre the window
        w, h = 560, 680
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._build_header()
        self._build_body()
        self._build_footer()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── header ───────────────────────────────────────────────────────────────
    def _build_header(self):
        hf = tk.Frame(self.root, bg=self.SAFFRON, height=6)
        hf.pack(fill="x")

        logo_frame = tk.Frame(self.root, bg=self.CHARCOAL, pady=32)
        logo_frame.pack(fill="x")

        # Bus emoji in a rounded box
        icon_bg = tk.Frame(logo_frame, bg=self.SAFFRON, width=72, height=72,
                           relief="flat", bd=0)
        icon_bg.pack()
        icon_bg.pack_propagate(False)
        tk.Label(icon_bg, text="🚌", font=("Segoe UI Emoji", 30),
                 bg=self.SAFFRON).place(relx=.5, rely=.5, anchor="center")

        tk.Label(logo_frame, text="BUSZIN",
                 font=("Georgia", 32, "bold"),
                 fg=self.SAFFRON, bg=self.CHARCOAL).pack(pady=(12, 2))

        tk.Label(logo_frame, text="Tamil Nadu's Premier Bus Network",
                 font=("Helvetica", 12), fg=self.MUTED,
                 bg=self.CHARCOAL).pack()

    # ── body ─────────────────────────────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self.root, bg=self.CHARCOAL, padx=40)
        body.pack(fill="both", expand=True)

        # ── status card ──
        card = tk.Frame(body, bg="#252545", bd=0, relief="flat")
        card.pack(fill="x", pady=(8, 20))
        inner = tk.Frame(card, bg="#252545", padx=24, pady=24)
        inner.pack(fill="x")

        self.status_icon  = tk.Label(inner, text="⏳", font=("Segoe UI Emoji", 22),
                                     bg="#252545", fg=self.WHITE)
        self.status_icon.grid(row=0, column=0, rowspan=2, padx=(0,16))

        self.status_title = tk.Label(inner, text="Starting server…",
                                     font=("Helvetica", 13, "bold"),
                                     fg=self.WHITE, bg="#252545", anchor="w")
        self.status_title.grid(row=0, column=1, sticky="w")

        self.status_sub   = tk.Label(inner, text="Please wait",
                                     font=("Helvetica", 11),
                                     fg=self.MUTED, bg="#252545", anchor="w")
        self.status_sub.grid(row=1, column=1, sticky="w")

        # ── animated progress bar ──
        pb_frame = tk.Frame(body, bg="#252545", height=6, bd=0)
        pb_frame.pack(fill="x", pady=(0, 4))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Saffron.Horizontal.TProgressbar",
                        troughcolor="#252545",
                        background=self.SAFFRON,
                        thickness=6,
                        borderwidth=0)
        self.pbar = ttk.Progressbar(pb_frame, style="Saffron.Horizontal.TProgressbar",
                                    mode="indeterminate", length=480)
        self.pbar.pack(fill="x")
        self.pbar.start(12)

        # ── feature pills ──
        features = [
            ("🔍", "Smart Bus Search",     "Autocomplete for all TN cities"),
            ("💺", "Seat Selection",       "Interactive seat map"),
            ("🍱", "In-Journey Meals",     "Pre-order food onboard"),
            ("💳", "Secure Payments",      "Card · UPI · Net Banking · Wallet"),
            
            ("🎫", "Booking History",      "All your tickets in one place"),
        ]
        pills_frame = tk.Frame(body, bg=self.CHARCOAL)
        pills_frame.pack(fill="x", pady=(8, 0))

        for i, (em, title, desc) in enumerate(features):
            row, col = divmod(i, 2)
            pill = tk.Frame(pills_frame, bg="#1E1E3A", padx=14, pady=10, bd=0)
            pill.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            pills_frame.grid_columnconfigure(col, weight=1)

            tk.Label(pill, text=em, font=("Segoe UI Emoji", 16),
                     bg="#1E1E3A", fg=self.WHITE).grid(row=0, column=0, rowspan=2, padx=(0,10))
            tk.Label(pill, text=title, font=("Helvetica", 11, "bold"),
                     fg=self.WHITE, bg="#1E1E3A", anchor="w").grid(row=0, column=1, sticky="w")
            tk.Label(pill, text=desc,  font=("Helvetica", 9),
                     fg=self.MUTED,  bg="#1E1E3A", anchor="w").grid(row=1, column=1, sticky="w")

        # ── launch button ──
        self.launch_btn = tk.Button(
            body, text="🚌  Launch BUSZIN App",
            font=("Helvetica", 14, "bold"),
            bg=self.GREEN_MID, fg=self.WHITE,
            activebackground=self.GREEN_DARK, activeforeground=self.WHITE,
            relief="flat", bd=0, padx=24, pady=14,
            cursor="hand2", state="disabled",
            command=self._open_browser
        )
        self.launch_btn.pack(fill="x", pady=(20, 8))

        self.reopen_btn = tk.Button(
            body, text="↩  Re-open in Browser",
            font=("Helvetica", 11),
            bg="#252545", fg=self.MUTED,
            activebackground="#1E1E3A", activeforeground=self.WHITE,
            relief="flat", bd=0, padx=20, pady=10,
            cursor="hand2", state="disabled",
            command=self._open_browser
        )
        self.reopen_btn.pack(fill="x", pady=(0, 4))

    # ── footer ───────────────────────────────────────────────────────────────
    def _build_footer(self):
        sep = tk.Frame(self.root, bg="#333355", height=1)
        sep.pack(fill="x")
        foot = tk.Frame(self.root, bg=self.CHARCOAL, pady=14)
        foot.pack(fill="x")
        tk.Label(foot, text="Made with ❤️ in Chennai  ·  © 2025 BUSZIN  ·  Python 3",
                 font=("Helvetica", 10), fg=self.MUTED,
                 bg=self.CHARCOAL).pack()

    # ── server launch ─────────────────────────────────────────────────────────
    def _start_server_thread(self):
        try:
            self.server = start_server(self.port)
            self.root.after(0, self._on_server_ready)
        except Exception as e:
            self.root.after(0, lambda: self._on_server_error(str(e)))

    def _on_server_ready(self):
        self.pbar.stop()
        self.pbar.configure(mode="determinate", value=100)
        self.status_icon.config(text="✅")
        self.status_title.config(text="Server running!", fg="#4CAF50")
        self.status_sub.config(text=f"Listening on  {self.url}")
        self.launch_btn.config(state="normal", bg=self.SAFFRON,
                               activebackground="#E65100")
        self.reopen_btn.config(state="normal")
        # auto-open browser
        self._open_browser()

    def _on_server_error(self, msg):
        self.pbar.stop()
        self.status_icon.config(text="❌")
        self.status_title.config(text="Server error", fg="#EF5350")
        self.status_sub.config(text=msg[:60])

    def _open_browser(self):
        webbrowser.open(self.url)
        self.status_title.config(text="App opened in browser ✓", fg="#4CAF50")
        self.status_sub.config(text="Return here to re-open or quit")

    # ── run ───────────────────────────────────────────────────────────────────
    def run(self):
        threading.Thread(target=self._start_server_thread, daemon=True).start()
        self.root.mainloop()

    def _on_close(self):
        if self.server:
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        self.root.destroy()

# ─────────────────────────── ENTRY POINT ─────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🚌  BUSZIN — Tamil Nadu Bus Booking System")
    print("=" * 55)
    try:
        app = BuszinLauncher()
        app.run()
    except Exception as e:
        # Headless fallback (no display)
        print(f"\n  ℹ  Tkinter not available ({e})")
        print("  Falling back to browser-only mode...\n")
        port   = find_free_port()
        server = start_server(port)
        url    = f"http://127.0.0.1:{port}"
        print(f"  ✅ Server started on {url}")
        print("  🌐 Opening in browser…\n")
        time.sleep(0.4)
        webbrowser.open(url)
        print("  Press Ctrl+C to quit.\n")
        try:
            while True: time.sleep(60)
        except KeyboardInterrupt:
            server.shutdown()
            print("\n  👋 BUSZIN closed. Safe travels!\n")
