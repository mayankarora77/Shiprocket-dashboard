"""
config.py: EDIT THIS FILE PER COMPANY.
All operational numbers are synthetic.
Only items in CONTEXT are based on public Shiprocket information.
"""

COMPANY = {
    "name": "Shiprocket",
    "logo_text": "SR",
    "product": "Shiprocket",
    "title": "Shiprocket Logistics Intelligence Dashboard",
    "subtitle": "Shipping · Fulfillment · Delivery Performance · AI-powered Insights",
    "accent": "#FF6B35",
    "period_label": "Today",
    "prepared_by": "Prototype by MAYANK",
    "disclaimer": "Concept prototype built from public Shiprocket information. "
                  "All operational figures are synthetic and do not represent Shiprocket's internal data.",
}


# Domain terminology used by the existing dashboard
LABELS = {
    "unit": "Region",
    "partner": "Courier Partners",
    "booking": "Shipments",
    "eta": "Avg Delivery Time (min)",
}


SIDEBAR_NAV = [
    "Overview",
    "Live Shipments",
    "Courier Performance",
    "Delivery Quality",
    "Regional Insights",
    "AI & Automation",
    "Reports",
]


# Synthetic KPI values for the prototype dashboard
KPIS = [
    {
        "label": "Total Shipments",
        "value": "18,420",
        "delta": "+16%",
        "note": "vs same time yesterday",
        "icon": "📦",
        "good_when": "up",
    },
    {
        "label": "Active Courier Partners",
        "value": "31",
        "delta": "+8%",
        "note": "currently available",
        "icon": "🚚",
        "good_when": "up",
    },
    {
        "label": "Avg. Delivery Time",
        "value": "2.8 days",
        "delta": "-12%",
        "note": "vs last week",
        "icon": "⏱️",
        "good_when": "down",
    },
    {
        "label": "RTO Rate",
        "value": "8.4%",
        "delta": "-19%",
        "note": "vs last week",
        "icon": "↩️",
        "good_when": "down",
    },
]


# Synthetic regional shipment data
#
# name, current shipments, expected demand, active courier partners,
# avg delivery time, RTO %, utilization %, latitude, longitude,
# change vs last week %
UNITS = [
    ("Delhi NCR",  3280, 3650, 34, 2.1,  6.8, 84, 28.6139, 77.2090, 18),
    ("Mumbai",     2940, 3200, 31, 2.5,  7.4, 81, 19.0760, 72.8777, 15),
    ("Bengaluru",  2760, 3020, 29, 2.3,  6.1, 87, 12.9716, 77.5946, 21),
    ("Hyderabad",  1980, 2160, 24, 2.7,  8.2, 78, 17.3850, 78.4867, 13),
    ("Chennai",    1760, 1880, 22, 2.9,  7.9, 76, 13.0827, 80.2707, 11),
    ("Pune",       1650, 1800, 21, 2.4,  6.5, 82, 18.5204, 73.8567, 16),
    ("Kolkata",    1240, 1420, 18, 3.4, 10.8, 69, 22.5726, 88.3639,  8),
    ("Ahmedabad",  1020, 1180, 17, 3.1,  9.4, 72, 23.0225, 72.5714,  7),
]


# Synthetic hourly shipment demand
HOURLY = {
    "hours": [
        "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
        "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM",
        "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
    ],

    "demand": [
        120, 180, 260, 340, 430, 520,
        610, 670, 720, 780, 860, 940,
        1020, 1080, 1040, 920, 760, 580
    ],

    "partners": [
        160, 210, 280, 350, 420, 500,
        570, 620, 650, 700, 760, 820,
        890, 930, 900, 820, 710, 620
    ],
}


# Status rules used by alerts and recommendations
THRESHOLDS = {
    "attention_gap_pct": 20,
    "attention_eta": 4.0,
    "monitor_gap_pct": 8,
    "monitor_cancel": 10,
}


# Public information about Shiprocket.
# These are the only factual company-specific items used in this prototype.
CONTEXT = [
    (
        "42+",
        "courier partners and 19,000+ pin codes supported across its shipping network",
        "Shiprocket official website / Fulfillment"
    ),
    (
        "AI",
        "Sense uses AI-driven capabilities for address verification, delivery accuracy and RTO reduction",
        "Shiprocket official website"
    ),
    (
        "Fastrr Assist",
        "AI shopping assistant for product and order queries, recommendations and multilingual conversations",
        "Shiprocket Product Highlights, Aug 2026"
    ),
    (
        "Fastrr Ads",
        "AI-powered advertising platform using commerce and purchase-behaviour signals for D2C brands",
        "Shiprocket Product Highlights, Aug 2026"
    ),
]


CONTEXT_TAKEAWAY = (
    "Shiprocket operates across shipping, fulfillment, checkout, customer engagement "
    "and AI-powered commerce products. This prototype focuses on shipment demand, "
    "courier capacity, delivery performance, regional gaps and potential AI-driven "
    "operational insights."
)