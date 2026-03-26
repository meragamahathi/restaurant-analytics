# Restaurant Analytics Dashboard
# Works with ANY dataset — columns auto-detected
# Stack: Streamlit · Plotly · Folium

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import io
from streamlit_folium import st_folium

st.set_page_config(page_title="Restaurant Analytics", page_icon="\U0001f37d\ufe0f",
                   layout="wide", initial_sidebar_state="expanded")

# ── Embedded default dataset ───────────────────────────────────
DEFAULT_CSV = 'Name,City,Region,Cuisines,Rating,Votes,Cost for Two,Online Delivery,Table Booking,Google Maps URL\nParampara flavours of india,Hyderabad,South,"North Indian, South Indian, Chinese, Desserts, Beverages",4.7,1263.0,1996,Yes,No,https://maps.app.goo.gl/6jfJFpE9YWjEXd5GA\nSo The Sky Kitchen,Hyderabad,South,Multi-cuisine,3.9,7744.0,2157,No,Yes,https://maps.app.goo.gl/yMrydwNFj62dsMES9?g_st=awb\nJewel of Nizam,Hyderabad,South,Indian,3.7,1585.0,1051,Yes,Yes,https://maps.app.goo.gl/fSowELEgc6gMP9az6\nAnandobrahma,Hyderabad,South,North Indian,4.3,2084.0,649,No,No,https://maps.app.goo.gl/y2tQvnS2dBou4TKa8\nBawarchi Restaurant,Hyderabad,South,North Indian,4.3,5403.0,1751,No,No,https://maps.app.goo.gl/ajaeaJ7VsfD5rSDr9?g_st=awb\nIshtaa -vegetarian Cuisine,Hyderabad,South,Andhra,3.7,4792.0,2346,No,No,https://maps.app.goo.gl/ZqeuprEW1KNijFJUA\nBlue Sea Restaurant,Hyderabad,South,Indian,4.8,7699.0,1027,No,No,https://maps.app.goo.gl/sZQNqRzSS7qwLm8z6\nCafe Bahar,Hyderabad,South,North Indian,4.7,5595.0,1542,No,Yes,https://maps.app.goo.gl/gsWCp5rEeR85tzRz8?g_st=awb\nBy The Bay,Hyderabad,South,North Indian,4.4,737.0,252,No,Yes,https://maps.app.goo.gl/UgMdJpExkPEDS3jk7\nGrand Hotel,Hyderabad,South,Multi-cuisine,3.6,3617.0,812,Yes,No,https://maps.app.goo.gl/mwVauCSDQund3Cpc6\nParadise,Hyderabad,South,Multi-cuisine,4.3,1610.0,2026,No,Yes,https://maps.app.goo.gl/AkT4hRivJBGoEuj67?g_st=awb\nPathemari kerala Restaurant,Hyderabad,South,Italian,4.1,738.0,832,No,Yes,https://maps.app.goo.gl/aFpB4SfV2BU7kiWA7\nMandi Manzil Multi Cusine Restaurant,Hyderabad,South,Andhra,4.8,3976.0,2053,Yes,No,https://maps.app.goo.gl/CYkxxzVD2ZWn1QkZ8\nMehfil Restaurant,Hyderabad,South,Indian,3.9,2216.0,2209,No,No,https://maps.app.goo.gl/Z7sjAnuSGeq5PDLfA\nArabian Spice Restaurant,Hyderabad,South,Indian,4.2,8593.0,707,Yes,Yes,https://maps.app.goo.gl/Sz4ot7EK3giXHAU18\nBesta -The Indian Kitchen,Vijayawada,East,Andhra,4.5,200.0,1741,Yes,No,https://maps.app.goo.gl/Pj76bumrqogLATRA7\nUnited Food Palace,Vijayawada,East,Andhra,4.5,2931.0,2336,No,No,https://maps.app.goo.gl/fPoRnmh4gqKn13PN9\nThrayam Restaurant,Vijayawada,East,Multi-cuisine,3.8,1837.0,281,Yes,No,https://maps.app.goo.gl/9tuV6fCxwSxiq9bm7\nCross Roads Restaurant,Vijayawada,East,Andhra,4.1,8651.0,2109,Yes,Yes,https://maps.app.goo.gl/ST7DGjsntpEidD6P8\nBheemasala Family Restaurant,Vijayawada,East,Andhra,4.6,9255.0,2392,Yes,No,https://maps.app.goo.gl/7xpLUUqYgxG42bAs8\nRusted Spoon,Vijayawada,East,Fast Food,4.4,8679.0,2141,Yes,No,https://maps.app.goo.gl/tEFKtiX4s3jnksLc9\nKK Restaurant,Vijayawada,East,Biryani,4.7,5653.0,1823,Yes,Yes,https://maps.app.goo.gl/9CUXkNyVUSXQWKUU8\nRR Dubbar,Vijayawada,East,Multi-cuisine,3.6,9307.0,1108,No,No,https://maps.app.goo.gl/uThD66aLFQ7gESnp6\nDelhi Highway Restaurant Vijayawada,Vijayawada,East,Italian,4.1,1878.0,518,No,Yes,https://maps.app.goo.gl/MqWMAZEVBk4wRtWR7\nFood Republic,Vijayawada,East,South Indian,3.8,2589.0,2337,Yes,Yes,https://maps.app.goo.gl/tgcM2HhV3PaTaR8Y7\nPlatform 65 The Train Theme Restaurant,Vijayawada,East,South Indian,4.5,3510.0,1439,Yes,No,https://maps.app.goo.gl/qv3WCAMp6WPdcbTd7\nSouthern Spice Family Restaurant&Conference Halls,Vijayawada,East,North Indian,4.6,5944.0,1348,Yes,No,https://maps.app.goo.gl/DKmxqS6cTbhJQXmh6\nAsian Food Bowl Restaurant,Vijayawada,East,Italian,4.5,3970.0,1592,Yes,Yes,https://maps.app.goo.gl/A64KA82pqaGpT7WPA\nTinadam A Multi Cuisine Restaurant,Vijayawada,East,South Indian,4.9,8509.0,560,No,Yes,https://maps.app.goo.gl/3ZQFb8YA2FacnQDq7\nMinerva Grand Restaurant,Vijayawada,East,Andhra,3.6,3134.0,1723,Yes,No,https://maps.app.goo.gl/2JkB48qfXn2nwcZ89\nAndhra Spice Restaurant,Vijayawada,East,Chinese,4.6,1221.0,473,Yes,Yes,https://maps.app.goo.gl/gmhzpVAKymygoyiu8\nHeaven\'s Park Arabian Multi Cuisine Restaurant Chennai,Chennai,South,North Indian,4.8,8123.0,813,Yes,No,https://maps.app.goo.gl/xuph3MABGFGtT2Ao8\nSix \' O\' one,Chennai,South,Multi-cuisine,3.7,6911.0,1887,No,No,https://maps.app.goo.gl/zS8r3UztaQNr2Dy86\nBroken Bridge CafÃ© Indian Restaurant,Chennai,South,North Indian,3.7,2622.0,703,No,No,https://maps.app.goo.gl/LL8qLLQgZwMriQ699\nPumpkin Tales Restaurant -Alwarpet,Chennai,South,Multi-cuisine,4.8,2334.0,2380,No,No,https://maps.app.goo.gl/6sMbyfy6bdTELjZc8\nMadras Spice Restaurant,Chennai,South,Italian,4.5,740.0,2293,No,No,https://maps.app.goo.gl/rQr6KFyWQVj9ZvBj7\nThe Waterfall Restaurant,Chennai,South,North Indian,4.5,4010.0,408,No,No,https://maps.app.goo.gl/UWK3em9wL87UHt2K7\n"Zaitoon Restaurant,Royapettah",Chennai,South,South Indian,4.8,7103.0,451,No,Yes,https://maps.app.goo.gl/62cXd9KEJgzxGtaF7\nEast Coastat Madras Square,Chennai,South,Italian,3.6,5823.0,575,Yes,Yes,https://maps.app.goo.gl/SfA52C2ovaBdmjJy7\nSeasonal Tastes,Chennai,South,Fast Food,4.8,1402.0,824,No,Yes,https://maps.app.goo.gl/ywSTWZiBS44Eouuk6\nPaprika,Chennai,South,Chinese,3.8,4971.0,679,No,No,https://maps.app.goo.gl/4RHJwwBu6PVkW5Sa7\nBoard Walk The Reataurant,Chennai,South,Chinese,4.1,2955.0,869,No,Yes,https://maps.app.goo.gl/E3Jd5oPzLHn9mk168\nNandhana Palace-Andhra Style Restaurant,Chennai,South,Italian,4.7,1162.0,2189,Yes,No,https://maps.app.goo.gl/axRjXqXCTWVpmxMD7\nOPM 2.O -Rooftop Restaurant Chennai,Chennai,South,Italian,3.5,9803.0,1467,Yes,Yes,https://maps.app.goo.gl/wPBnf2S5h7a6vF7W7\nPadmam Veg Restaurant,Chennai,South,Chinese,4.6,4076.0,1788,No,No,https://maps.app.goo.gl/YRAFD75NViKyJgeq5\nBuhari - Mount Road,Chennai,South,Chinese,4.1,2669.0,1010,No,Yes,https://maps.app.goo.gl/6DGih5pQqWouZMJXA\nCoal Barbecues,Chennai,South,Multi-cuisine,4.5,8506.0,536,Yes,Yes,https://maps.app.goo.gl/EBe77Q3PQYrcAU3Q9\nNational Durbar Restaurant,Chennai,South,Chinese,4.8,1568.0,1450,No,No,https://maps.app.goo.gl/RP5VcJCAoiswGACt5\nChilli Malli South IndianRestaurant,Chennai,South,Biryani,4.5,7542.0,2289,Yes,No,https://maps.app.goo.gl/oUThi7ddcLqfy5EP7\nAnnalakshmi Restaurant,Chennai,South,South Indian,4.5,6165.0,203,Yes,Yes,https://maps.app.goo.gl/StEfxFZJUJhzXFm5A\nClassic Curry Point Zone 149,Mumbai,West,Chinese,4.8,9923.0,1577,Yes,No,https://maps.google.com/?q=Classic+Curry+Point+Zone+149\nLake View CafÃ©,Mumbai,West,North Indian,4.3,8490.0,672,Yes,No,https://maps.app.goo.gl/PvdLc8qdZSBbo2kCA\nThe Bombay  Canteen,Mumbai,West,Chinese,4.8,601.0,876,No,Yes,https://maps.app.goo.gl/SZ1Se1X2tuxbC7h19\nPeshwa Pavilion,Mumbai,West,Andhra,4.2,429.0,1809,No,Yes,https://maps.app.goo.gl/PrEpdFbtT4TmFfoW6\nShamiana,Mumbai,West,North Indian,3.8,6446.0,2252,No,Yes,https://maps.app.goo.gl/aLPcEVjeyZKqpHsm9\nGallops Restaurant,Mumbai,West,South Indian,3.9,4756.0,268,No,Yes,https://maps.app.goo.gl/4ruay85PVMTHaNNN9\nSeven Kitchens,Mumbai,West,Biryani,3.9,6730.0,2301,Yes,No,https://maps.app.goo.gl/aYZWWiGMuMMv7GZk7\nGajalee,Mumbai,West,Biryani,4.8,3382.0,1778,Yes,No,https://maps.app.goo.gl/VxHsRn77KQLJn9Qn9\nTanatan Shivaji Park,Mumbai,West,Italian,4.3,104.0,1288,No,No,https://maps.app.goo.gl/LHNY926Cv7evSRh58\n"Kyani & Co. | Legendary Irani Restaurant, Bakers",Mumbai,West,Multi-cuisine,3.6,6480.0,295,No,Yes,https://maps.app.goo.gl/4gYFC9UVvC6Ly1Du8\nTrishna,Mumbai,West,Multi-cuisine,3.7,8677.0,1563,Yes,No,https://maps.app.goo.gl/yKxMwwLMn2bnLr159\nPrithvi CafÃ©,Mumbai,West,South Indian,4.3,5688.0,1369,Yes,No,https://maps.app.goo.gl/j1faCJAKpFUqVu6y8\nAmazonia,Mumbai,West,Indian,3.8,9640.0,2017,No,Yes,https://maps.app.goo.gl/u9BzAb5AP8pXDgHv6\nFifty Five East,Mumbai,West,Fast Food,3.7,1953.0,232,Yes,No,https://maps.app.goo.gl/rqTSscH2Z6F4sdZU6\nShalimar Restaurant,Mumbai,West,North Indian,3.6,8095.0,2113,No,No,https://maps.app.goo.gl/4n4GkdADWJfdYWje9\nDelhi highway,Mumbai,West,Multi-cuisine,4.9,7330.0,472,Yes,Yes,https://maps.app.goo.gl/KHMLh7C4ZSKjvbXYA\nO Pedro - BKC,Mumbai,West,Biryani,4.5,8215.0,1925,Yes,Yes,https://maps.app.goo.gl/btEkq5cng9mibAgK6\nBy The Mekong,Mumbai,West,Indian,3.5,9152.0,1503,No,No,https://maps.app.goo.gl/7SjWfUn1iqYZoRjr9\nGaylord Restaurant,Mumbai,West,Chinese,4.2,2825.0,1230,No,Yes,https://maps.app.goo.gl/xfoiBS8hXpuFpUv66\nThe Earth Plate,Mumbai,West,North Indian,4.9,2109.0,850,Yes,No,https://maps.app.goo.gl/mfQwGzVzvYfp6DH89\nThe Table,Mumbai,West,Multi-cuisine,4.7,1097.0,1285,Yes,No,https://maps.app.goo.gl/GEM1uNQ4W55CW87D9\nNawab Saheb,Mumbai,West,Italian,4.5,3403.0,2264,No,No,https://maps.app.goo.gl/Ua7Qk86kyc45yorYA\nLeopold CafÃ©,Mumbai,West,South Indian,4.2,8298.0,1209,No,No,https://maps.app.goo.gl/ff7Fus7vbJqy7kAZ6\nPONDICHÃ\x89RY CAFÃ\x89 - ALL-DAY DINING,Mumbai,West,South Indian,4.8,3828.0,2226,Yes,Yes,https://maps.app.goo.gl/PXfC59EHmhMP6s8eA\nYauatcha Mumbai,Mumbai,West,Andhra,4.2,9888.0,2020,Yes,No,https://maps.app.goo.gl/ZnWsXbBzyy9xGwPL9\nCinCin Mumbai,Mumbai,West,Fast Food,4.8,2440.0,990,Yes,No,https://maps.app.goo.gl/aadZ7D4Ekuvq3q1w6\nKhyber,Mumbai,West,Multi-cuisine,4.7,9317.0,2119,Yes,Yes,https://maps.app.goo.gl/PQzPo4sVRxtaZn1Y\nMocambo Restaurant and Bar,Kolkata,East,Biryani,3.9,1802.0,1402,No,Yes,https://maps.app.goo.gl/DVPmJaD7pEBa9u576\nPeter Cat,Kolkata,East,North Indian,3.8,9405.0,284,No,Yes,https://maps.app.goo.gl/ChpDRZdyhyfDibeHA\nSpice Kraft,Kolkata,East,Italian,4.1,5935.0,1434,Yes,No,https://maps.app.goo.gl/sRPtJhNdP3od5gF1A\nNizam\'s Restaurant,Kolkata,East,Italian,3.6,3203.0,2308,Yes,Yes,https://maps.app.goo.gl/yfVHMfwdhab4S9V9A\nSri Delight Center 180,Kolkata,East,Indian,4.2,8939.0,511,Yes,No,https://maps.google.com/?q=Sri+Delight+Center+180\nGolden Joy Restaurant,Kolkata,East,Multi-cuisine,4.4,2048.0,437,No,Yes,https://maps.app.goo.gl/SL5sm8wLAHe3FSVb9\nKasturi,Kolkata,East,Biryani,4.0,2466.0,1751,Yes,Yes,https://maps.app.goo.gl/xpKPmJcpSYBkMmmJ7\nCalcutta Retro,Kolkata,East,North Indian,3.7,5973.0,2368,No,No,https://maps.app.goo.gl/eLL4KxZFXfYdh4B78\nThe Bridge,Kolkata,East,Multi-cuisine,4.5,4024.0,1055,No,Yes,https://maps.app.goo.gl/b74sZ17JUz458eSe8\nEden Pavilion - ITC Sonar,Kolkata,East,Italian,4.4,5918.0,1993,Yes,Yes,https://maps.app.goo.gl/3VopZ4Nci95VFcZ67\nSufi Palace,Kolkata,East,Fast Food,3.8,9261.0,1673,No,No,https://maps.app.goo.gl/t3jUiydpFFRLoHmJ6\nSorano,Kolkata,East,Biryani,3.6,7811.0,2014,No,No,https://maps.app.goo.gl/Ru72wpMA4MR27SRQ6\nKoji,Pune,West,Biryani,3.9,7306.0,204,Yes,No,https://maps.app.goo.gl/AYzn6Ype13FqAnWP7\nMalaka Spice,Pune,West,Chinese,3.5,7283.0,1561,No,No,https://maps.app.goo.gl/mFMcMzjwoojab8AW7\nLe Plaisir,Pune,West,Multi-cuisine,3.5,4915.0,1453,Yes,Yes,https://maps.app.goo.gl/3oDzbbsP1kojJrdv5\n"World Of Veg - Rooftop Restaurant, Ramsukh House",Pune,West,South Indian,4.6,8641.0,2107,Yes,Yes,https://maps.app.goo.gl/GWhH6YtCyETbXr4P9\nSpice Kitchen,Pune,West,Chinese,4.4,5678.0,1910,Yes,Yes,https://maps.app.goo.gl/y7F5Ta9XbeiVg3ew5\nPaasha,Pune,West,Indian,4.5,9615.0,2176,No,Yes,https://maps.app.goo.gl/RCF7AFZHZgeEPefG8\n1000 Oaks,Pune,West,Biryani,4.7,7137.0,2142,No,No,https://maps.app.goo.gl/vhdk4Zaf1E9xRV9m9\nBlue Nile RestauranBlue Nile Restaurant,Pune,West,Multi-cuisine,3.6,2533.0,1984,Yes,Yes,https://maps.app.goo.gl/jCBiN5ZKfuQPuwpK9\nAl DI LA - Rooftop Restaurant In Pune,Pune,West,Indian,3.5,7315.0,1424,No,No,https://maps.app.goo.gl/AMuw7Jgi9nyYdvdNA\nYakii | Asian Restaurant | Sushi | Dimsums | Cocktails | Brunch,Pune,West,South Indian,3.5,8807.0,1532,Yes,No,https://maps.app.goo.gl/jTn6bngH3KqW7zHS8\nPersian Darbar Pune,Pune,West,Chinese,3.6,1732.0,1075,Yes,Yes,https://maps.app.goo.gl/bdFnYZz8ycEbJsYy6\nGeorge Restaurant,Pune,West,Chinese,3.9,6734.0,1863,Yes,No,https://maps.app.goo.gl/Reuzz7aoNzSqwDZ19\nSavya Rasa,Pune,West,Indian,3.8,2733.0,592,No,Yes,https://maps.app.goo.gl/9Yd4jTd9MFhByvU46\nMaa Aathidyam,Tirupati,South,Biryani,4.4,1714.0,2448,No,No,https://maps.app.goo.gl/ZMAKpWTg2sfgkBjK9\nPlantain Leaf Restaurant,Tirupati,South,Indian,3.5,7015.0,1724,No,No,https://maps.app.goo.gl/31hehrMEffy5VyodA\nGufha Restaurant,Tirupati,South,Chinese,4.6,8184.0,2426,No,Yes,https://maps.app.goo.gl/5BfZTrd64gdPP4gQA\nVivaha Bhojanambu,Tirupati,South,North Indian,3.5,9720.0,1811,No,Yes,https://maps.app.goo.gl/gt7vVzgnUYXgLqp1A\nRobo Diner,Tirupati,South,Fast Food,3.5,316.0,1264,No,No,https://maps.app.goo.gl/vYm9ksfghX1zjiWL8\nRayalaseema spice,Tirupati,South,Indian,4.8,6330.0,950,No,Yes,https://maps.app.goo.gl/ccd7uDszpkuCfnJs6\nMINT Restaurant,Tirupati,South,Italian,4.2,4249.0,2048,Yes,No,https://maps.app.goo.gl/qPWaKR7BVuP6uVo47\nTaaza Kitchen,Tirupati,South,Multi-cuisine,4.4,589.0,2288,No,Yes,https://maps.app.goo.gl/KNrR6X3D9BHqpzQ48\nSubbayya Gari HotelÂ,Tirupati,South,South Indian,4.5,5645.0,2412,No,Yes,https://maps.app.goo.gl/3DKFbfgzGj9Gmq3s5\nANNAMAYYA ANNASALA,Tirupati,South,South Indian,4.6,1280.0,392,No,Yes,https://maps.app.goo.gl/pNLfoX4adXuLtJpQ9\nBarbeque Nation,Tirupati,South,Italian,4.3,3148.0,780,Yes,Yes,https://maps.app.goo.gl/Tw72WGukryEwHEi2A\nSouthern Spice,Tirupati,South,South Indian,4.8,3988.0,835,Yes,Yes,https://maps.app.goo.gl/m9MpmWToy4FYNT4g6\nBlue Fox,Tirupati,South,Multi-cuisine,4.5,3819.0,637,No,Yes,https://maps.app.goo.gl/K4tyCw1xyQo26je68\nThe Paradise family restaurant,Tirupati,South,South Indian,4.5,8698.0,1178,No,Yes,https://maps.app.goo.gl/du9YJtuNzkCQMUun8\nChillies Restaurant,Tirupati,South,Chinese,4.3,754.0,1382,No,No,https://maps.app.goo.gl/y7DeFArYK6jadhRK7\nSri Lakshmi Narayana Bhavan,Tirupati,South,Multi-cuisine,4.6,2491.0,722,Yes,No,https://maps.app.goo.gl/eZM7e9nEyWMJDmPk8\nKomala Vilas,Nellore,South,North Indian,4.9,1397.0,1594,No,Yes,https://maps.app.goo.gl/JW2QpnQVrxMZB7Va7\nRayalaseema Military Hotel,Nellore,South,Italian,4.5,6026.0,1566,No,No,https://maps.app.goo.gl/JFvEHBLyDQyUtfVb9\nRaju Gari Kodi Pulao,Nellore,South,Fast Food,3.9,4979.0,2437,Yes,Yes,https://maps.app.goo.gl/Hp4vS97sTULU8CdF8\nThe Mint Multicuisine Restaurant,Nellore,South,Andhra,3.7,2470.0,701,No,No,https://maps.app.goo.gl/qPWaKR7BVuP6uVo47\nMayuri Family Restaurant,Nellore,South,Multi-cuisine,3.9,1740.0,1252,Yes,No,https://maps.app.goo.gl/SvKGK3jD6XbdvaB79\nMurali Krishna 70 Ac Restaurant,Nellore,South,Fast Food,4.9,7102.0,1413,No,Yes,https://maps.app.goo.gl/edcxsn4k1qrhfRk28\nSitara Restaurant,Nellore,South,Multi-cuisine,4.2,3975.0,2339,Yes,Yes,https://maps.app.goo.gl/vgYry6UrntdsB99g6\nGuma Gumalu Authentic Restaurant,Nellore,South,Andhra,4.6,9787.0,2326,No,Yes,https://maps.app.goo.gl/59sNTyQ3MxDKzGrF9\nNaidu Gari Kunda Biryani,Nellore,South,Indian,3.8,3316.0,484,Yes,Yes,https://maps.app.goo.gl/C7ArjXN5r3gcJpDbA\nHotel Rayalseema\'s,Nellore,South,Biryani,4.5,9838.0,1247,No,No,https://maps.app.goo.gl/SR7QqckPRmiF5M9MA\nAmaravathi Family Restaurant,Nellore,South,Biryani,3.7,980.0,245,No,No,https://maps.app.goo.gl/84wpFXXQxSNJusQv9\nSimhapuri Family Dhaba,Nellore,South,Multi-cuisine,4.5,7079.0,683,No,Yes,https://maps.app.goo.gl/Q2yr4i7HXnG8XsM5A\nPrakriti Multicuisine Restaurant,Nellore,South,North Indian,4.6,4563.0,782,No,No,https://maps.app.goo.gl/XiGL3kFJjNi7BwwQ8\nchef street,Nellore,South,Andhra,4.2,5060.0,1691,No,Yes,https://maps.app.goo.gl/U9fthdAtwCaY4JGo6\nThe Legends,Bangalore,South,South Indian,4.8,6548.0,1267,Yes,No,https://maps.app.goo.gl/zgdMmXT5ae8XyW8q6\nThe Palms Brew and Kitchen,Bangalore,South,Italian,4.6,3062.0,895,Yes,Yes,https://maps.app.goo.gl/4VdqiaTd2J4MDpa69\nSpice Terrace,Bangalore,South,Multi-cuisine,3.9,7744.0,2157,No,Yes,https://maps.app.goo.gl/AXkyAzPkDyP25sscA\nMaya Bangalore,Bangalore,South,South Indian,4.0,4770.0,1534,No,No,https://maps.app.goo.gl/EmdpAwuiZzfk7s6y9\nNarmada Restaurant,Bangalore,South,Italian,4.0,1480.0,2477,Yes,Yes,https://maps.app.goo.gl/cPagDJvxToBNnD3i7\nAnTeRa Kitchen,Bangalore,South,Fast Food,3.8,6943.0,614,Yes,No,https://maps.app.goo.gl/q3oWFsq4vE9ar1FT8\nFlavours of Andhra,Bangalore,South,Chinese,4.3,3964.0,2172,Yes,No,https://maps.app.goo.gl/YNrrDSxREjTUf4GY6\nThe Pump House,Bangalore,South,Fast Food,4.7,2992.0,2462,Yes,Yes,https://maps.app.goo.gl/viAP95aRG3cBsLiy7\nNeemsi Restaurant,Bangalore,South,Chinese,3.5,2412.0,1762,Yes,No,https://maps.app.goo.gl/AnFCcgtfk5tJhQW57\nAdvaita RestaurantÂ,Bangalore,South,Fast Food,4.0,8708.0,1412,Yes,No,https://maps.app.goo.gl/iMU6ABGyg1Uhwujb7\nGardenwoods Rooftop Kitchen,Bangalore,South,Indian,4.0,5155.0,1542,Yes,No,https://maps.app.goo.gl/tMpsNHW3D6PvYppu7\nMILAN\'S RESTAURANT,Bangalore,South,Biryani,4.3,5221.0,1934,No,No,https://maps.app.goo.gl/MJE3QMak6si2411b7\nMaffei Kitchen,Bangalore,South,Italian,4.8,538.0,2250,No,Yes,https://maps.app.goo.gl/77YDsSAQrSW998fF8\nKaravali Fine Dine Restaurant,Bangalore,South,Multi-cuisine,4.4,1655.0,824,Yes,No,https://maps.app.goo.gl/8wWSQCc1K1KYvNTw5\nCastle Restaurant,Bangalore,South,Biryani,4.9,3533.0,1928,Yes,Yes,https://maps.app.goo.gl/ARK2spGbCmGnM1KL7\nThe Big Buffet,Bangalore,South,Biryani,4.1,4529.0,764,Yes,No,https://maps.app.goo.gl/EHu2sUsyHHu6kDqW7\nNandhana Palace,Bangalore,South,Multi-cuisine,4.4,5053.0,2120,Yes,Yes,https://maps.app.goo.gl/tWzygrvz8xicer1bA\nMayuri,Bangalore,South,Chinese,4.4,9973.0,664,No,No,https://maps.app.goo.gl/NstTk4C4L9yzNzga8\nBombay Brasserie,Bangalore,South,Multi-cuisine,3.8,8592.0,919,No,Yes,https://maps.app.goo.gl/jgWytPEJnvdp8jLD6\nHotel Jas Vizag,Vizag,South,Andhra,4.7,3715.0,1790,Yes,Yes,https://maps.app.goo.gl/vrzPJ12AtWfvrUv28\nCelebrations Restaurant,Vizag,South,South Indian,4.0,4770.0,1534,No,No,https://maps.app.goo.gl/UAxo1PXtjwBptw9H6\nWelcomeCafe Oceanic Restaurant,Vizag,South,Italian,4.0,1480.0,2477,Yes,Yes,https://maps.app.goo.gl/tnCGtojQ7EECGuwP6\nMaaya,Vizag,South,Fast Food,3.8,6943.0,614,Yes,No,https://maps.app.goo.gl/L9WG7YySMRnCuQPE7\nZamindari Restaurant,Vizag,South,Chinese,4.3,3964.0,2172,Yes,No,https://maps.app.goo.gl/uYGJkPTqH5WHrtBd9\nUpland Bistro,Vizag,South,Fast Food,4.7,2992.0,2462,Yes,Yes,https://maps.app.goo.gl/V4Hq68iWrm4HrR3aA\nCascades Restaurant,Vizag,South,Chinese,3.5,2412.0,1762,Yes,No,https://maps.app.goo.gl/Pu89qQR3EM8rEbaSA\nMayabazar Restaurant,Vizag,South,Fast Food,4.0,8708.0,1412,Yes,No,https://maps.app.goo.gl/RwwH33KQPmQzi9tM7\nBarkaas Arabic Restaurant,Vizag,South,Indian,4.0,5155.0,1542,Yes,No,https://maps.app.goo.gl/NFtgMitUakpffYLaA\n"Zurii - Lounge,Dine, Bar & Restaurant",New Delhi,North,Biryani,4.3,5221.0,1934,No,No,https://maps.app.goo.gl/KLHvJX7xChRo7iik6\nIndian Accent,New Delhi,North,Italian,4.8,538.0,2250,No,Yes,https://maps.app.goo.gl/cKaMZnp3iW5hakkq8\nThe Imperial Spice,New Delhi,North,Multi-cuisine,4.4,1655.0,824,Yes,No,https://maps.app.goo.gl/ZdnvR9GGDWKLoYSJ9\nBukhara,New Delhi,North,Biryani,4.9,3533.0,1928,Yes,Yes,https://maps.app.goo.gl/Hr5ExU6tcUzsw5ut9\nWhite Oak Restaurant,New Delhi,North,Biryani,4.1,4529.0,764,Yes,No,https://maps.app.goo.gl/nszEHTzwk3sJEJ8Y8\nDiggin  CafÃ©,New Delhi,North,Multi-cuisine,4.4,5053.0,2120,Yes,Yes,https://maps.app.goo.gl/FitYtDzjHZqRceZQA\nTamara Restaurant,New Delhi,North,Chinese,4.4,9973.0,664,No,No,https://maps.app.goo.gl/JtWjyYSJzZQPsQHb8\nSomewhere Delhi,New Delhi,North,Multi-cuisine,3.8,8592.0,919,No,Yes,https://maps.app.goo.gl/S7P87p7KfKQr69c5A\nKwality,New Delhi,North,Chinese,4.8,7053.0,1216,No,Yes,https://maps.app.goo.gl/jZByBwWiNyKUgwvN6\nTamasha,New Delhi,North,Indian,4.4,1741.0,1739,No,Yes,https://maps.app.goo.gl/eU8kuZQA4LGYP7ot7\nFarzi CafÃ©,New Delhi,North,Multi-cuisine,3.6,484.0,1156,Yes,No,https://maps.app.goo.gl/VENh8dm4UeXGpgRF6\nAmour Bistro,New Delhi,North,Biryani,4.7,7981.0,2380,No,Yes,https://maps.app.goo.gl/9T5NnqYPNRqBcpZi9\nDaryaganj Restaurant,New Delhi,North,Italian,3.6,4052.0,2141,Yes,No,https://maps.app.goo.gl/WGHvp4LUqen5bjx77\nMysore CafÃ©,New Delhi,North,Multi-cuisine,4.2,6206.0,1178,Yes,Yes,https://maps.app.goo.gl/iG4TGncnBM8CWQoh9\nParikrama The Revolving Restaurant,New Delhi,North,South Indian,4.3,8854.0,2261,No,Yes,https://maps.app.goo.gl/8P4KfQwfVFK4ES8a7\nAdbhutam CafÃ©,New Delhi,North,South Indian,3.7,5822.0,1462,Yes,No,https://maps.app.goo.gl/5KsyfkPABrexofKG9\nGulati Restaurant,New Delhi,North,South Indian,4.6,410.0,1161,Yes,Yes,https://maps.app.goo.gl/2KXwGzkoGa6mCcyPA\nSevilla,New Delhi,North,Fast Food,4.6,7063.0,2410,No,Yes,https://maps.app.goo.gl/7KhiuogncMzxdUiH8\nMayura Gardenia,Kadapa,South,Fast Food,4.3,2181.0,2085,No,No,https://maps.app.goo.gl/f25AeKVhYL81RPLy9\nFirdouse pure Veg & Non-Veg,Kadapa,South,Chinese,4.5,8506.0,1560,No,No,https://maps.app.goo.gl/3kLMQ1uDTE6c2xQZA\nSitara Garden Family Restaurant,Kadapa,South,Biryani,3.6,6340.0,540,No,No,https://maps.app.goo.gl/9q6UZvAcvF9GHYfK9\nZaitoon Multicuisine Restaurant,Kadapa,South,Andhra,4.1,5283.0,1322,Yes,Yes,https://maps.app.goo.gl/1Y5usdBYW59ChiND6\nGrand Family Restaurant,Kadapa,South,Andhra,4.3,1578.0,1492,Yes,Yes,https://maps.app.goo.gl/D64vRcZVwfMp2vfk9\nMadhavi\'s Kitchen,Kadapa,South,South Indian,4.7,1089.0,1332,No,No,https://maps.app.goo.gl/D64vRcZVwfMp2vfk9\nChikkis CafÃ© &Resto,Kadapa,South,Andhra,4.2,8886.0,1898,No,No,https://maps.app.goo.gl/Vddv2zzerYE5rWFU6\nBarbeque Nation,Kadapa,South,Indian,3.5,2185.0,1954,No,Yes,https://maps.app.goo.gl/UukhabWAMqxBY3b2A\nBahar CafÃ©,Kadapa,South,Indian,4.3,6729.0,1601,Yes,No,https://maps.app.goo.gl/GtVTfLUsPgnKCFFKA\nBrundavan Spicy Restaurant,Kadapa,South,Andhra,4.5,8036.0,807,No,No,https://maps.app.goo.gl/b9Sv6DwfLNjiqEWH6\nLeirung Restro,Imphal,East,South Indian,4.3,6391.0,446,Yes,Yes,https://maps.app.goo.gl/xRtvmKFnvyRZfu8w7\nMint,Imphal,East,Biryani,3.8,4925.0,1751,No,Yes,https://maps.app.goo.gl/k13exFN5bT7VLNUU6\nHarvest CafÃ© Kitchen,Imphal,East,Chinese,4.3,6855.0,2418,Yes,Yes,https://maps.app.goo.gl/Wh6MqJuWqZF4Pg2Y8\nLe Zara Imphal,Imphal,East,North Indian,4.3,6811.0,1176,No,No,https://maps.app.goo.gl/pMNKv8pwjNo8aL8a7\nEden lounge Imphal,Imphal,East,Biryani,3.6,284.0,1161,Yes,No,https://maps.app.goo.gl/try61DtiCDrVLZZQ6\nSawadee Restaurant,Imphal,East,Italian,4.0,5080.0,2319,No,Yes,https://maps.app.goo.gl/2ygCRuJBhKBTKEnv5\nCrush Imphal,Imphal,East,Andhra,4.8,2012.0,1887,No,No,https://maps.app.goo.gl/YtMQU8KSM7UNHJSU9\nAgashiye,Ahmedbad,West,Andhra,4.7,1861.0,1244,No,No,https://maps.app.goo.gl/k8dGMAT86S59t9q99\nUnder The Neem Trees,Ahmedbad,West,Fast Food,4.3,1010.0,1588,Yes,Yes,https://maps.app.goo.gl/wRfukcsuwELAsjN2A\nGordhan Thal,Ahmedbad,West,Indian,3.5,3373.0,1076,Yes,Yes,https://maps.app.goo.gl/sVzNm2nbHV93P9KY6\nTinello,Ahmedbad,West,Multi-cuisine,4.5,5288.0,752,Yes,No,https://maps.app.goo.gl/LYpsEpbtQvf3tcmKA\nRajwadu,Ahmedbad,West,Andhra,4.3,7272.0,1880,Yes,No,https://maps.app.goo.gl/v8x3TNj7nFBxny1W7\nIsharaa,Ahmedbad,West,Chinese,4.8,9923.0,1577,Yes,No,https://maps.app.goo.gl/SJ7ritmjXzrujyVK8\nPeacock Restaurant,Jaipur,North-west,North Indian,4.4,8857.0,1477,Yes,No,https://maps.app.goo.gl/8amp1YKnGu4BjThMA\nSkyfall Restaurant,Jaipur,North-west,"Chinese,Italian,North Indian",4.3,6491.0,1688,Yes,No,https://maps.app.goo.gl/8amp1YKnGu4BjThMA\nGovindam Retreat,Jaipur,North-west,Multi-cuisine,4.4,5053.0,2120,Yes,Yes,https://maps.app.goo.gl/ca5WYk8Bvogjr3KU6\nKalyan Restaurant&Bar,Jaipur,North-west,Rajasthani cuisine,4.4,9973.0,664,No,No,https://maps.app.goo.gl/cFqtGSoyAguwjREo9\nHawk View Restaurant &Bar,Jaipur,North-west,Multi-cuisine,3.8,8592.0,919,No,Yes,https://maps.app.goo.gl/h9FDXHxssdFmZ2BVA\nDragon House,Jaipur,North-west,chineese,4.8,7053.0,1216,No,Yes,https://maps.app.goo.gl/744xnp5E9exyeDLK7\nMonarch Restaurant,Jaipur,North-west,Multi-cuisine,4.4,1741.0,1739,No,Yes,https://maps.app.goo.gl/2BxEdn3eaomWYcLV6\nAnnpoornam - Best South Indian Restaurant,Jaipur,North-west,South Indian,3.6,484.0,1156,Yes,No,https://maps.app.goo.gl/5g4Xs58xxq6vEndJ7\nGiardino,Jaipur,North-west,Italian,4.4,8857.0,1477,Yes,No,https://maps.app.goo.gl/9J1Ymcxkj4WK1iT36\nSupreme Restaurant,Venkatagiri,South,Multi-cuisine,4.4,4562.0,864,No,Yes,https://maps.app.goo.gl/kiuoggqrZ7prsCpB8\nGreen Park Family Dhaba&Restaurant,Venkatagiri,South,Biryani,4.3,4311.0,1741,Yes,Yes,https://maps.app.goo.gl/Qea4DKvP3HaKE68W8\nMama\'s Kitchen Family Restaurant,Venkatagiri,South,Fast Food,3.9,2504.0,1344,No,No,https://maps.app.goo.gl/S1D9TJZ4xJmCCx498\nKarthikeya Kitchen Hub Family Dhaba&Restaurant,Venkatagiri,South,Chinese,4.9,2500.0,1630,No,Yes,https://maps.app.goo.gl/ZmthcDdynhdt8ZMLA\nFood N Fun A/C,Venkatagiri,South,Fast Food,4.5,9231.0,1100,No,No,https://maps.app.goo.gl/Pq2MGgo6z6Pn5YcA6\nPV Mess,Venkatagiri,South,Indian,4.1,1258.0,1587,No,Yes,https://maps.app.goo.gl/4XEyXcDHx4ukanFE7\nReddamma Tiffins,Venkatagiri,South,Biryani,4.1,5271.0,2369,Yes,No,https://maps.app.goo.gl/Hsv2vfKwyD3TFAoG8\nRadha Krishna Restaurant,Venkatagiri,South,Italian,5.0,147.0,2463,No,No,https://maps.app.goo.gl/FqTUbRz7ZVwEPAJc8\nKakatiya Family Restaurant,Venkatagiri,South,Multi-cuisine,5.0,2504.0,1595,Yes,No,https://maps.app.goo.gl/makh9n8FudBpYUj2A\nNaidu(Tiffins&Fast food),Venkatagiri,South,Biryani,3.8,1487.0,1937,Yes,Yes,https://maps.app.goo.gl/VtLk3oRUH8QCuSjYA\nAbhiruchi Family Restaurant,Venkatagiri,South,Biryani,4.2,2200.0,389,Yes,Yes,https://maps.app.goo.gl/tnQerjB5Y3ZqAcuKA\nNawabz Empire Fine Dine Restaurant,Venkatagiri,South,Multi-cuisine,4.7,7040.0,2210,No,No,https://maps.app.goo.gl/VrEGSmr5CtEcdZNYA\nNarayana Dhaba,Venkatagiri,South,Dhaba,4.0,9622.0,1652,No,No,https://maps.app.goo.gl/ws9qhDzF3WbmGSUG7\nBismillah Bhai Biriyani,Venkatagiri,South,Fast Food,5.0,919.0,618,Yes,Yes,https://maps.app.goo.gl/1STLtd2GeA4YUqtW7\nNaidu Gari Kunda Biryani,Bhimavaram,South,Biriyani,4.7,2666.0,679,No,Yes,https://maps.app.goo.gl/7mz8aVwXpg6zrgvz7\nMV Royal Spice,Bhimavaram,South,Biriyani,4.7,8767.0,2049,No,No,https://maps.app.goo.gl/PMP4YB4XGZHKB7uM9\nSuprabath Restaurant,Bhimavaram,South,Biriyani,4.0,8267.0,1930,Yes,No,https://maps.app.goo.gl/4JBSShbzzdKey91G7\nCafÃ© Brew &Bake,Bhimavaram,South,Asian,4.5,491.0,1023,No,No,https://maps.app.goo.gl/c3DE4ziqEk9QuSDn9\nPichayya Hotel,Bhimavaram,South,Multi-cuisine,4.5,1855.0,974,No,Yes,https://maps.app.goo.gl/mgEA8kGc1ukBiGXY7\nSitayya Family Restaurant,Bhimavaram,South,Multi-cuisine,4.0,220.0,1259,Yes,No,https://maps.app.goo.gl/Rkn9jBBMto2jYD6D6\nFRYDO,Bhimavaram,South,Mexican,4.2,8851.0,2104,No,No,https://maps.app.goo.gl/tKs4c5g1EGLQw4HaA\nBiriyani and More,Bhimavaram,South,Biriyani,4.1,984.0,1404,Yes,Yes,https://maps.app.goo.gl/NFXfihUP17PDfvGz9\nChandrika Biriyani Family point,Bhimavaram,South,Biriyani,4.0,7135.0,1191,No,No,https://maps.app.goo.gl/6jogrthnLqYhfPKt8\nAbhiruchi Restaurant,Bhimavaram,South,Andhra,3.7,4638.0,2088,Yes,Yes,https://maps.app.goo.gl/M5QpNYiv9EpUuBVj7\nGrillland,Bhimavaram,South,Multi-cuisine,4.3,8745.0,2222,No,Yes,https://maps.app.goo.gl/4XjSBgsvz8LM6qrQ8\nHarshitha Kitchen,Bhimavaram,South,Biriyani,4.5,8113.0,209,Yes,Yes,https://maps.app.goo.gl/7kQZmB8VWUh9wHyp8\nJai Sri Restaurant &Meal,Bhimavaram,South,Multi-cuisine,4.1,2906.0,1104,No,No,https://maps.app.goo.gl/Fnz2m2PgPhGnCPdw6\nThe Udhayam CafÃ©,Bhimavaram,South,vegetarian,4.3,8701.0,2442,No,Yes,https://maps.app.goo.gl/nWSUv9eYAq2eAcYz8\nAroma\'s Kitchen,Bhimavaram,South,Multi-cuisine,4.6,156.0,771,Yes,Yes,https://maps.app.goo.gl/TXMFp3qUxMKu2wev8\nRamu Hotel And Venkateswara Kirana,Bhimavaram,South,Andhra,4.1,170.0,354,Yes,Yes,https://maps.app.goo.gl/MWQPv8bBxDrDgk946\nSpice Magic,Bhimavaram,South,Biriyani,3.8,5729.0,2266,No,Yes,https://maps.app.goo.gl/tTdAVLPYcHgX4jDX9\nVikranth Family Restaurant,Bhimavaram,South,Multi-cuisine,4.3,4.8,1105,Yes,no,https://maps.app.goo.gl/asCnMYjZTYBMGJex5\nBengaluru Bhavan,Bhimavaram,South,vegetarian,4.4,9758.0,2156,No,No,https://maps.app.goo.gl/9QagroyDN1UYQkXp7\nHotel Sridevi,Bhimavaram,South,South Indian,3.7,3987.0,1064,No,Yes,https://maps.app.goo.gl/RMdt6Mt92sv7G9SM7\nZeeshan Biriyani,Bhimavaram,South,Multi-cuisine,4.8,2744.0,399,Yes,No,https://maps.app.goo.gl/Wu8tS8w5ZfEuAk4x7\nThe Shawarma Co,Bhimavaram,South,Shawarma Restaurant,4.2,8008.0,800,No,No,https://maps.app.goo.gl/HFYMJyWCiwFrDVAn8\nAlimas Hyderabadi Biriyani And Kababs,Bhimavaram,South,Biriyani,4.0,4024.0,1055,No,Yes,https://maps.app.goo.gl/M4MYGxamZ7aWPf5U8\nBhuvana Vijayam Durbar,Bhimavaram,South,Multi-cuisine,4.2,5918.0,1993,Yes,Yes,https://maps.app.goo.gl/hFuyLC4nC1Jq29CR6\nFood Treat,Bhimavaram,South,Multi-cuisine,4.9,9261.0,1673,No,No,https://maps.app.goo.gl/Yyn8nPeFW3UX3sTD6\nSoba Sassy,Kolkata,East,Chinese,4.3,7234.0,1220,Yes,Yes,https://maps.app.goo.gl/BTkqB7acqp1mL5p36\nBAR-B-Q RESTAURANT,Kolkata,East,Chinese,4.4,9900.0,2200,No,Yes,https://maps.app.goo.gl/dCiiJKMjwWuW9MjY7\nHard Rock Cafe,Kolkata,East,American,4.4,4300.0,1550,Yes,Yes,https://maps.app.goo.gl/rnFasBkzPo9kx1du5\nJam House,Kolkata,East,North Indian,4.1,938.0,1050,Yes,Yes,https://maps.app.goo.gl/cuXpSGLPKN2KK5E17\n"Barbeque Nation- Park Street, Kolkata",Kolkata,East,Barbeque,4.5,6543.0,2550,Yes,Yes,https://maps.app.goo.gl/ePutYiXXUShMh9z29\nFlame And Grill,Kolkata,East,Buffet,4.4,5132.0,2550,Yes,Yes,https://maps.app.goo.gl/wfDUj9ng5dZvbYC26\nPeshawri -ITC Sonar,Kolkata,East,North Indian,4.5,4362.0,2341,No,Yes,https://maps.app.goo.gl/EY6noj2fFj7B2JAy9\nSocial Kitchen,Kolkata,East,Multi-cuisine,4.4,2874.0,1800,Yes,Yes,https://maps.app.goo.gl/tNvybF9w2QoiM2WY9\nKwalityÂ,Kolkata,East,North Indian,4.2,1456.0,1350,Yes,Yes,https://maps.app.goo.gl/cGm36KLXrejZZaYK9\nSabir\'s,Kolkata,East,Biryani,3.9,4387.0,2550,Yes,Yes,https://maps.app.goo.gl/DYiYB3J8zDjJvb8dA\nAminia,Kolkata,East,Biryani,4.0,3457.0,1560,Yes,Yes,https://maps.app.goo.gl/QLEuEsaiJefFn4H19\nOh! Calcutta,Kolkata,East,Bengali cuisine,4.1,5897.0,3400,Yes,Yes,https://maps.app.goo.gl/RDrRZAoen8Xm9EmDA\nBhojohori Manna,Kolkata,East,Traditional Bengali,4.2,4384.0,2200,Yes,Yes,https://maps.app.goo.gl/hYMY6MtjpxMCRMNFA\nKewpies,Kolkata,East,Traditional Bengali,4.3,5365.0,2150,Yes,Yes,https://maps.app.goo.gl/Q7s3cJgDTcQcfxB99\nKoshe KoshaÂ,Kolkata,East,Bengali cuisine,4.0,6453.0,2550,Yes,Yes,https://maps.app.goo.gl/2AZoucJxNwzuGqzYA\nSaptapadi,Kolkata,East,Traditional Bengali,4.2,7362.0,1240,Yes,Yes,https://maps.app.goo.gl/VRMEH3ZAvMasHFFQ9\nVertex - The Liquid Restaurant,Kolkata,East,Elite Indian,4.3,5737.0,2200,Yes,Yes,https://maps.app.goo.gl/uoHt9RMeaub7HpZD8\nThe Skypoint,Kolkata,East,Bengali cuisine,4.2,6338.0,2600,Yes,Yes,https://maps.app.goo.gl/Vrm2mW5GHBuxnJCd9\nGrand Market Pavilion,Kolkata,East,Bengali cuisine,4.1,5372.0,2000,Yes,Yes,https://maps.app.goo.gl/ZdH65WPo36dm7xqN6\nYauatcha,Kolkata,East,Modern Cantonese,4.2,6842.0,1850,Yes,Yes,https://maps.app.goo.gl/RQvhxi9oh1Tjy3xq5\nPa Pa YaÂ,Kolkata,East,Modern Asian,3.8,4282.0,1500,Yes,Yes,https://maps.app.goo.gl/W2H89qsng68ZFvoV6\nFarzi Cafe,Kolkata,East,Modern Indian,3.9,3526.0,1800,Yes,Yes,https://maps.app.goo.gl/vsoCSxWMDPYS79hu9\nBlue & Beyond,Kolkata,East,Asian cuisine,4.0,5733.0,1700,Yes,Yes,https://maps.app.goo.gl/WAf24CQ6RsKmL99w6\nArsalan,Kolkata,East,Biryani,4.4,5473.0,1050,Yes,No,https://maps.app.goo.gl/mS6bmHoFVWZrR9S77\nMainland China,Kolkata,East,Chinese,3.8,3728.0,800,Yes,No,https://maps.app.goo.gl/F4ig3TSjxUoNYeNN6\nAtmosphere 6,Pune,West,Grill,4.1,3637.0,2100,Yes,Yes,https://maps.app.goo.gl/FGh8HPE6ZDELmgKt7\nWorld Of Veg - Rooftop Restaurant,Pune,West,Vegetarian,4.1,5737.0,2200,Yes,Yes,https://maps.app.goo.gl/4yHb1XfeRKHKwHee8\nThe Sassy Spoon,Pune,West,Multi-cuisine,4.3,3743.0,1550,Yes,Yes,https://maps.app.goo.gl/fySRyAuUE4vsNFUq9\n"The Urban Foundry, Baner",Pune,West,Multi-cuisine,4.3,3284.0,1600,Yes,Yes,https://maps.app.goo.gl/rCQX66WHKoZkkuvg7\nSavya Rasa,Pune,West,South Indian,4.5,4734.0,2000,Yes,Yes,https://maps.app.goo.gl/LnS4QWo9eC69dihX7\nCopaCabana,Pune,West,Multi-cuisine,4.4,5373.0,2300,Yes,Yes,https://maps.app.goo.gl/3kT2YrBZqZx1WHFXA\nThe Camden Lane,Pune,West,Vegetarian,4.2,5473.0,1800,Yes,Yes,https://maps.app.goo.gl/PMSwwhMuxKJhzNvC6\nVaishali Restaurant,Pune,West,South Indian,4.2,3844.0,1300,Yes,Yes,https://maps.app.goo.gl/hNTYY1rjdaT7RM5v8\nPersian Darbar Pune,Pune,West,Persian,4.1,5536.0,2250,Yes,Yes,https://maps.app.goo.gl/SLWShqwVqazQA4My8\nPaashh,Pune,West,Organic,4.5,3829.0,2840,Yes,Yes,https://maps.app.goo.gl/A1L317cie5tdAsoa6\nAcai Pune,Pune,West,Multi-cuisine,4.1,3244.0,1250,Yes,Yes,https://maps.app.goo.gl/2h8YxZYoZGZv43zP9\nVohuman Cafe,Pune,West,CafÃ©,4.1,3433.0,1000,Yes,Yes,https://maps.app.goo.gl/cLgj8YU391BB7ftT6\nThe House of Medici,Pune,West,Multi-cuisine,4.3,4672.0,1400,Yes,Yes,https://maps.app.goo.gl/jvcSPjCqpMtBZ6Vp6\nChingari,Pune,West,North Indian,4.3,5382.0,2200,Yes,Yes,https://maps.app.goo.gl/dx8YXgQu3vMyY94b6\nBluefrog,Pune,West,European cuisine,4.2,3727.0,2500,Yes,Yes,https://maps.app.goo.gl/uZ2dzMNtFE4GLzTL7\nLittle Italy,Pune,West,Italian,4.3,3823.0,3200,Yes,Yes,https://maps.app.goo.gl/24DwM6QfjZSJaSkQ6\nAlto VinoÂ,Pune,West,Italian,4.2,2746.0,2330,Yes,Yes,https://maps.app.goo.gl/4Xz9owyk2kyz7FtB6\nKangan,Pune,West,Indian,4.3,4772.0,1550,Yes,Yes,https://maps.app.goo.gl/mAgohGynRcBhHoKH9\nBaan Tao,Pune,West,Multi-cuisine,4.5,3722.0,3646,Yes,Yes,https://maps.app.goo.gl/uQTZ3fXmds8CfDVx8\nCopper Chimney,Pune,West,North Indian,4.2,3223.0,2100,Yes,Yes,https://maps.app.goo.gl/pviBJJyUyDYKroVXA\nShahji\'s Paratha House,Pune,West,North Indian,4.0,4244.0,1200,Yes,Yes,https://maps.app.goo.gl/gxntCzuy4W1XaPUz9\nHindavi Swaraj,Pune,West,Maharashtrian,4.3,5546.0,1500,Yes,Yes,https://maps.app.goo.gl/HTiBXVFaWPLHDAXW8\nMaratha Samrat,Pune,West,Maharashtrian,4.2,3282.0,2000,Yes,Yes,https://maps.app.goo.gl/o6XCM7LXw2a84AEn7\nCafÃ© Maroo,Pune,West,Korean,3.8,3853.0,1500,Yes,Yes,https://maps.app.goo.gl/2dqXgvzEWhC2E72m7\nCafÃ© Peter,Pune,West,Korean,4.0,4473.0,2000,Yes,Yes,https://maps.app.goo.gl/2v132tdK3k6wiMiC6\nKINI (Korean Indian Noodle Inn),Pune,West,Korean,4.2,5446.0,2200,Yes,Yes,https://maps.app.goo.gl/paadjEKafM3sybv96\nKimling,Pune,West,Chinese,4.0,4728.0,2000,Yes,Yes,https://maps.app.goo.gl/BQvcdjsttPs9HLLSA\nTwo Sticks,Pune,West,Chinese,4.1,2756.0,2200,Yes,Yes,https://maps.app.goo.gl/hFoyiv3S3K5W7YNK8\nRoman Dine,surat,west,Vegetarian,4.8,2746.0,2200,Yes,Yes,https://maps.app.goo.gl/NuqZTB2mCzrzLzDt6\nPavilion Restaurant,surat,west,Multi-cuisine,4.2,4772.0,2200,Yes,Yes,https://maps.app.goo.gl/LZ2boFAaRuSEepaF8\nSpice Petals,surat,west,Multi-cuisine,4.7,3722.0,2200,Yes,Yes,https://maps.app.goo.gl/NmUXEHzQvbbfEJ5U8\nEnjoy Restaurant,surat,west,South Indian,4.9,3223.0,2200,Yes,Yes,https://maps.app.goo.gl/BFPCGKxjPLtK42Zx5\nSpice Terrace Restaurant,surat,west,Multi-cuisine,4.5,4244.0,2200,Yes,Yes,https://maps.app.goo.gl/7pHZp7vvwGLup1iz9\nPRESTIGE ROOFTOP RESTAURANT,surat,west,Vegetarian,4.6,5546.0,2200,Yes,Yes,https://maps.app.goo.gl/m9q8uzgv9taTobqC6\nIt\'s Mirchi,surat,west,South Indian,4.8,3282.0,2200,Yes,No,https://maps.app.goo.gl/SJGpCMMANZQLoLoS8\nSpice Villa Restaurant,surat,west,Persian,4.4,3853.0,2200,Yes,No,https://maps.app.goo.gl/QVfPByfC1ir4UPx48\nKabir Restaurant,surat,west,Organic,4.5,4473.0,2200,Yes,No,https://maps.app.goo.gl/1pbbyg91Lv7xT3Rf7\nV - The Restaurant,surat,west,Multi-cuisine,4.2,5446.0,1500,Yes,No,https://maps.app.goo.gl/Mg564revz54rUJ4YA\nOran Restaurant & Banquets,surat,west,chinese,4.7,4728.0,1500,Yes,No,https://maps.app.goo.gl/PUa9VNyVToSbFbjE6\n4M\'s Kitchen,surat,west,Multi-cuisine,4.0,2756.0,1500,Yes,No,https://maps.app.goo.gl/ZVNcrgAQ1UD7yEb6A\nStories of South,surat,west,North Indian,4.5,6338.0,1500,Yes,No,https://maps.app.goo.gl/QWg724pBWuEKRLra8\nLet\'s Table Talk,surat,west,European cuisine,4.8,5372.0,1500,No,No,https://maps.app.goo.gl/Emp9YoLxaDhsgScE7\nBarbeque Nation,surat,west,Italian,4.3,6842.0,1500,No,No,https://maps.app.goo.gl/JZeLRXZjiNgGtNcB9\nSilvernest Restaurant,surat,west,Italian,4.2,4282.0,1500,No,Yes,https://maps.app.goo.gl/FyrEdqe4mUkAeD8G9\nAvadh Family Restaurant,surat,west,Indian,4.5,3526.0,1500,No,Yes,https://maps.app.goo.gl/ongYVRUacbNvFknu9\nWok On Fire,surat,west,Multi-cuisine,4.6,5733.0,1500,No,Yes,https://maps.app.goo.gl/NWZCiCPnpetva84z7\nThe Bungalow Cafe,surat,west,North Indian,4.8,5473.0,1500,No,Yes,https://maps.app.goo.gl/EHum5F2SRbxtXEWP6\nMaharaja Restaurant,surat,west,North Indian,4.4,3728.0,1200,No,Yes,https://maps.app.goo.gl/KB4LQd6MrcYx7Gav7\nThalaivaa The South Indian Restaurant,surat,west,South Indian,4.5,3637.0,1200,No,Yes,https://maps.app.goo.gl/9tNa1uTELYm6ne598\nWelcomCafe,Guntur,south,Buffet,4.2,5737.0,1200,No,Yes,https://maps.app.goo.gl/EFGRSq1kN1eopptB8\nFlechazo Buffet Restaurant & Banquets,Guntur,south,Buffet,4.7,3743.0,1400,Yes,Yes,https://maps.app.goo.gl/TSq1KmptCs7uV1c79\nHungry Daddy,Guntur,south,Multi-cuisine,4.0,3284.0,800,Yes,No,https://maps.app.goo.gl/tYPy5NXS9ghTt5YN8\nAL Ajaib Restaurant,Guntur,south,North Indian,4.5,4734.0,2000,Yes,No,https://maps.app.goo.gl/gHJkgucZXv2co1B27\nRose Cafe,Guntur,south,Fast Food,4.8,3987.0,1600,Yes,No,https://maps.app.goo.gl/D3NGEVz75FT8ZsfN9\nMourya Tasty Foods,Guntur,south,South Indian,4.3,2744.0,1200,Yes,No,https://maps.app.goo.gl/cS9nF9MkjjQhthjC8\nViceroy Biryani Point,Guntur,south,Biryani,4.5,8008.0,1000,Yes,No,https://maps.app.goo.gl/XhMxJ1R5QNk1kyfy7\nFlameingoes,Guntur,south,Multi-cuisine,4.5,4024.0,1150,Yes,No,https://maps.app.goo.gl/ubtnZLym7FPR3E758\nChennai Thalappatthi Family Restaurant,Guntur,south,South Indian,4.0,5918.0,1546,Yes,No,https://maps.app.goo.gl/3YPBiSZe5x5nTwDP8\nForque Kitchen & Cafe,Guntur,south,South Indian,4.2,9261.0,1200,Yes,No,https://maps.app.goo.gl/raKEWJvFwwpkiJ4H9\nAnand Bhavan,Guntur,south,South Indian,4.1,7234.0,1246,Yes,No,https://maps.app.goo.gl/GnhbJ11af6m3wz1UA\nAmogham,Guntur,south,Vegetarian,4.5,9900.0,1345,Yes,No,https://maps.app.goo.gl/n8G9wWHGvMvXViPY6\nThe Wagon Wheel,Guntur,south,Multi-cuisine,3.7,4300.0,1000,Yes,No,https://maps.app.goo.gl/sVCGww62MWfm1xkn8\nNavodaya Biriyani House,Guntur,south,Biryani,4.3,938.0,800,Yes,No,https://maps.app.goo.gl/AP3NMQirmCGmLg9G8\nMaqbi multi cuisine restaurant,Guntur,south,Multi-cuisine,4.5,6543.0,1200,No,yes,https://maps.app.goo.gl/AaNxvtwjQ3kXMqUi9\nNOVEL Hotel,Guntur,south,North Indian,4.1,5132.0,1200,No,yes,https://maps.app.goo.gl/WrtTWs6chXyAXFRY9\nGrill Nights,Guntur,south,Barbeque,4.3,4362.0,1200,No,yes,https://maps.app.goo.gl/u5hgTFLj6GZaRpHx5\nLazeez Multi Cuisine Restaurant,chittoor,south,South Indian,4.6,2874.0,800,No,yes,https://maps.app.goo.gl/bgpXe7MnMLJUSaub9\nWay To Food Restaurant,chittoor,south,Chinese,4.1,1456.0,900,No,yes,https://maps.app.goo.gl/fKmqbnLYC2cbkPeEA\nFarsi Flavours,chittoor,south,Multi-cuisine,4.9,4387.0,1000,No,yes,https://maps.app.goo.gl/V2sLmEuVAgT2h5Qs5\nNEW AROMA MULTICUISINE RESTAURANT,chittoor,south,Multi-cuisine,4.3,3457.0,1200,No,yes,https://maps.app.goo.gl/fk6P6YzF8jZXZA9R9\nMom\'s Kitchen,chittoor,south,South Indian,4.4,3526.0,800,No,No,https://maps.app.goo.gl/za2zzRAf4ruYqo8Q7\n369 Food Park & Family Restaurant,chittoor,south,Multi-cuisine,4.4,5733.0,700,No,No,https://maps.app.goo.gl/tGcxyj8FbKWfQJgx9\nRuchi Pure Veg Restaurant,chittoor,south,Vegetarian,4.1,5473.0,1000,yes,No,https://maps.app.goo.gl/Q9fQw1wWiAyitCHW8\nWizards Cuisine,chittoor,south,Indian,4.5,3728.0,1200,Yes,No,https://maps.app.goo.gl/PZVWE3XHox41aMFS6\nPhoenix Resto,chittoor,south,Biryani,4.4,3637.0,1000,Yes,No,https://maps.app.goo.gl/ajuUmZ3t81MeyE5X6\nClicKitchen Restaurant,chittoor,south,Andhra,4.5,5737.0,900,Yes,No,https://maps.app.goo.gl/cYsYurd5yGP19DPT7\nBhanu\'s SBV Family Restaurant,chittoor,south,Andhra,4.4,3743.0,1500,Yes,No,https://maps.app.goo.gl/Raqn4Q31cBiAbpLg6\nTrini Restaurant,chittoor,south,Multi-cuisine,4.2,3284.0,1000,Yes,No,https://maps.app.goo.gl/rszsoTokWJ9utfGM7\nLRS Restaurant,chittoor,south,South Indian,3.9,4734.0,2000,Yes,yes,https://maps.app.goo.gl/17Sceswm9RtPLd96A\nSalt N Pepper Snacks Corner,chittoor,south,Fast Food,4.0,5373.0,1000,Yes,yes,https://maps.app.goo.gl/XdVRsqqqFgXdxy689\nRk restaurant,Anantapur,south,South Indian,4.5,5473.0,500,yes,yes,https://maps.app.goo.gl/D3bSNPShRQfxEjVC9\nNalabheema Multi - Cuisine Fine Dine Restaurant,Anantapur,south,Multi-cuisine,4.7,3844.0,700,yes,No,https://maps.app.goo.gl/TipSpjdGXbNgoBJx9\nTASTE OF Pulao\'s Shreyas Grand,Anantapur,south,Multi-cuisine,4.3,5536.0,1000,yes,No,https://maps.app.goo.gl/mHC3iteCTiUgMwYXA\nRayala Restaurant,Anantapur,south,Andhra,4.0,3829.0,1200,Yes,Yes,https://maps.app.goo.gl/XpdSoYJn8xe6wZu99\nPower Restaurant veg/nonveg,Anantapur,south,Multi-cuisine,4.6,3244.0,1200,Yes,yes,https://maps.app.goo.gl/ewvjbfvZ8X6xHTSA8\nVivaha Bhojanambu,Anantapur,south,Vegetarian,4.4,3433.0,800,Yes,yes,https://maps.app.goo.gl/CPfeMQ7DXMVB1ZL7A\nMehfil Arabic Restaurant,Anantapur,south,Biryani,4.0,4672.0,3620,Yes,No,https://maps.app.goo.gl/QfoNGU42C1crCobx6\nNaidu Gari Kunda Biryani,Anantapur,south,Biryani,4.3,5382.0,1448,Yes,yes,https://maps.app.goo.gl/FdRQhR2HqQsFRZfW7\nTFM Sky Lounge,Anantapur,south,Multi-cuisine,4.3,2150.0,1300,No,Yes,https://maps.app.goo.gl/m2oiigLdbSfrBcPC9\nNirvana Multicuisine Restaurant,Anantapur,south,multi-cuisine,5.0,189.0,1300,yes,yes,https://maps.app.goo.gl/KK38HzQGHR9Pcs1t5\nExotikka,Anantapur,south,Multi-cuisine,4.1,2140.0,1300,yes,No,https://maps.app.goo.gl/Zeu4sx14SmxFrMA46\nRuchi\'s Family Restaurant,Anantapur,south,South Indian,3.8,3000.0,800,yes,yes,https://maps.app.goo.gl/29bXo98eYigcRwVW6\nThe Prison Jail Theme Restaurant,Anantapur,south,Biryani,3.9,4500.0,600,yes,yes,https://maps.app.goo.gl/2JxgAJ4NCc8AUabQ9\nPaakashala Anantapur,Anantapur,south,Indian,4.0,3780.0,800,yes,No,https://maps.app.goo.gl/vN3RMsbAJcxYucXX8\nRayalaseema Dabbawala,Anantapur,south,Andhra,4.6,3743.0,900,yes,No,https://maps.app.goo.gl/dM9dq4h74CqdwxBK6\nAmigos Food Club,Anantapur,south,Biryani,4.2,3284.0,900,yes,yes,https://maps.app.goo.gl/WR9yobjC7GhJkm126\nBite n Sip,Anantapur,south,Chinese,4.5,4734.0,900,yes,yes,https://maps.app.goo.gl/9vkE5jVTK2VPPi8U8\nSindhura Restaurant,Anantapur,south,South Indian,3.9,5373.0,1000,No,Yes,https://maps.app.goo.gl/7Ycm5GWBFdzzLXSB8\nMr. & Mrs. Rolls,Anantapur,south,Multi-cuisine,4.5,5473.0,500,No,Yes,https://maps.app.goo.gl/dD8UmPuPvX3WhRMz8\nG G Family Restaurant,Anantapur,south,Multi-cuisine,4.0,3844.0,900,No,No,https://maps.app.goo.gl/KBQb2PRgUfb5BGip6\nVIVA FINE DINE,kurnool,south,Multi-cuisine,4.7,5536.0,1200,No,No,https://maps.app.goo.gl/Luj4QJfpUF1WywMcA\nAiyana\'s Kitchen,kurnool,south,,4.9,3829.0,600,yes,Yes,https://maps.app.goo.gl/qcWvxswm1LfC5SA69\nOTG - Onthego Foodvibes,kurnool,south,,4.6,3244.0,900,No,No,https://maps.app.goo.gl/FsWT4aLVYUABWV2s9\nAjwa Exotica,kurnool,south,Biryani,4.7,3433.0,600,Yes,Yes,https://maps.app.goo.gl/XnYAY6ah3BNMSpvy5\nBhagini Hastha Restaurant,kurnool,south,Multi-cuisine,4.3,4672.0,1000,No,No,https://maps.app.goo.gl/C76XGTcrvmAinc9U6\nMythri family restaurant,kurnool,south,South Indian,4.0,5382.0,800,Yes,No,https://maps.app.goo.gl/Kf3e8mXcvCGgLUm2A\nSree Divya Family Restaurant,kurnool,south,South Indian,4.2,3727.0,1000,Yes,No,https://maps.app.goo.gl/89jyJfqRQnZjabfH7\nParadise Biryani,kurnool,south,Biryani,4.1,3823.0,900,No,No,https://maps.app.goo.gl/4MjcPRYfKPHtFp61A\nThe Magic Resto,kurnool,south,Pizza,4.2,2746.0,1300,No,Yes,https://maps.app.goo.gl/1BTqoEsycZtYbtRn7\nPrime Kitchen Restaurant,kurnool,south,Biryani,4.1,4772.0,800,Yes,Yes,https://maps.app.goo.gl/HrpCgxTskonqsbrF9\nUnlimited Multi Cuisine RestaurantÂ,kurnool,south,Multi-cuisine,4.3,3722.0,600,No,No,https://maps.app.goo.gl/38JtzHT9a1u5zMVT8\nAVIDHA RESTAURANT,kurnool,south,South Indian,4.5,3223.0,800,yes,Yes,https://maps.app.goo.gl/tPLRLtmSYgrNd8Eq5\nDARSHAN VEG RESTURANT,kurnool,south,Vegetarian,4.4,4244.0,750,yes,No,https://maps.app.goo.gl/oynRwCBfHt1YM7Md7\nkushas Kitchen,kurnool,south,South Indian,4.4,5546.0,1200,yes,Yes,https://maps.app.goo.gl/VorrDjJ8Uxs5RdLZ9\nTHE TEROTALE,Nashik,west,Vegetarian,4.5,3282.0,1550,No,Yes,https://maps.app.goo.gl/GUpVEoyANUK7CAbJ7\nmykonos,Nashik,west,Italian,4.7,2669.0,1600,No,Yes,https://maps.app.goo.gl/jLUQb7iAB461ENPp7\n21st Century Restaurant,Nashik,west,Indian,4.0,8506.0,2000,No,Yes,https://maps.app.goo.gl/gTdBg6cB4dczhypR8\nTales & Spirits Bistro,Nashik,west,European cuisine,4.4,1568.0,2300,No,Yes,https://maps.app.goo.gl/51MB1A7wakLVbVH79\nDil Se Desi,Nashik,west,North Indian,4.1,7542.0,1800,Yes,Yes,https://maps.app.goo.gl/ChFsAcmPHWQPvJDp8\nHotel Radhakrishna,Nashik,west,South Indian,4.0,6165.0,1300,No,No,https://maps.app.goo.gl/XurHLnnvcYSX6pYf7\nAnna\'s House of Dosa,Nashik,west,South Indian,4.7,9923.0,2250,Yes,Yes,https://maps.app.goo.gl/9KEEaiLKAiSP5Qqj6\nAl Arabian Express,Nashik,west,non vegetarian,4.4,8490.0,2840,yes,No,https://maps.app.goo.gl/jqRuaAeXdu1BcRtV6\nVeg Aroma,Nashik,west,Vegetarian,4.8,601.0,1250,yes,No,https://maps.app.goo.gl/wvL5UF7vRbTYeoqx7\nFlying Monk,Nashik,west,chinese,4.0,429.0,1000,yes,Yes,https://maps.app.goo.gl/NGTe8CtiSmNca7gY7\nHaldiram\'s,Nashik,west,Vegetarian,4.7,6446.0,1400,yes,Yes,https://maps.app.goo.gl/JZcVHJTVm4twAcJw8\nThe Second Empire,Nashik,west,North Indian,4.2,4756.0,2200,No,No,https://maps.app.goo.gl/g4SJyrgfnPpHyXqg9\nMajhali Restaurant,Nashik,west,sea food,4.3,6730.0,2500,Yes,No,https://maps.app.goo.gl/8fKEbe7RKMgsSAYS7\nASTER - MULTI-CUISINE RESTAURANT,Nashik,west,North Indian,4.5,3382.0,3200,Yes,Yes,https://maps.app.goo.gl/uvXV6tD2UXuaDc9b6\nCurry Leaves Pure VegÂ,Nashik,west,South Indian,4.6,4000.0,2330,Yes,No,https://maps.app.goo.gl/96fZAXRjcWtT7XKV7\nLarive kitchen and cocktail,Nashik,west,Vegetarian,4.3,6480.0,1550,No,No,https://maps.app.goo.gl/BY6Voi87BvT6h93VA\nThe Public House Restaurant,Bhopal,central,North Indian,4.3,3244.0,1000,yes,yes,https://maps.app.goo.gl/pyW3stCVWsPwdjV18\nWind And Waves Restaurant,Bhopal,central,South Indian,4.0,3433.0,800,Yes,No,https://maps.app.goo.gl/w2ybVQ2eBAzgRDKA8\nZa-Aiqa,Bhopal,central,Italian,4.8,4672.0,1200,Yes,Yes,https://maps.app.goo.gl/76aWspvh28sdaWi88\nIvoryy Bhopal,Bhopal,central,North Indian,4.5,5382.0,1600,No,Yes,https://maps.app.goo.gl/iGzgW8QvtbdXqMwu8\nFusion Cafe,Bhopal,central,North Indian,4.7,3727.0,1500,No,No,https://maps.app.goo.gl/6WATF12TJh3pxpyRA\nWazwan Restaurant,Bhopal,central,North Indian,4.7,3823.0,1400,Yes,Yes,https://maps.app.goo.gl/LXYEaG3JVJ3ko6i47\nGood Food Restaurant,Bhopal,central,South Indian,4.8,2746.0,1000,Yes,Yes,https://maps.app.goo.gl/oETQHUtoQdJqRqgG7\nPAGE 3 - Multi Cuisine Restaurant,Bhopal,central,Multi-cuisine,4.5,4772.0,600,No,No,https://maps.app.goo.gl/QJtMwyZxTxZyUPDL9\nPolka Restaurant,Bhopal,central,North Indian,4.7,3722.0,900,Yes,Yes,https://maps.app.goo.gl/CeVJVSvJMRSWiVVs9\nMantar Restaurant,Bhopal,central,North Indian,4.4,220.0,1000,No,No,https://maps.app.goo.gl/81bADwL1Zb4DbqQc9\nThe Brunch House,Bhopal,central,North Indian,4.3,8851.0,500,No,Yes,https://maps.app.goo.gl/CHGdvFygh6gyhdj47\nBHOPAL UDIPI RESTAURANT,Bhopal,central,South Indian,4.2,984.0,600,Yes,No,https://maps.app.goo.gl/emJc3sSLx3viBAmP9\nNaadbramha Idli,Bhopal,central,South Indian,4.8,7135.0,1100,No,Yes,https://maps.app.goo.gl/KTe1m9fFNUi5mxGK9\nRaj darbar,Bhopal,central,south Indian,4.6,4638.0,1300,Yes,Yes,https://maps.app.goo.gl/gQXBYXPiTF89XgFp7\nTaste of India,Bhopal,central,south Indian,4.2,8745.0,400,No,Yes,https://maps.app.goo.gl/b4XGaeLRwagrpTue9\nMITHO WOK STREET,Bhopal,central,Chinese,4.6,8113.0,1000,Yes,No,https://maps.app.goo.gl/m7T2x9uzdB3cjBbD6\nLil\' China,Bhopal,central,Chinese,4.9,2906.0,1200,No,No,https://maps.app.goo.gl/PEmEkV6iiBZq9cdh7\nManohar Dairy & Restaurant,Bhopal,central,Chinese,4.3,8701.0,700,Yes,Yes,https://maps.app.goo.gl/ki44h7EHaR2HAg7K9\nLittle Italy Restaurant,Bhopal,central,Italian,4.6,156.0,600,Yes,Yes,https://maps.app.goo.gl/vGxexNsGSaRv9Tp58\nSherwoods,Bhopal,central,multi-cuisine,4.8,170.0,800,Yes,No,https://maps.app.goo.gl/7CZfNJzVwrdgDk517\nSasural The Restro,Agra,west,North Indian,4.7,5729.0,900,Yes,Yes,https://maps.app.goo.gl/wK7fK9jpJW6XGy92A\nThe Nawaabs,Agra,west,North Indian,4.7,2000.0,1000,No,No,https://maps.app.goo.gl/mFpgZcHQgroYHULk6\n'

# ── Session state ─────────────────────────────────────────────
if "df"         not in st.session_state: st.session_state.df         = None
if "dark_mode"  not in st.session_state: st.session_state.dark_mode  = False
if "data_src"   not in st.session_state: st.session_state.data_src   = "default"

dark = st.session_state.dark_mode

# ── THEME VARIABLES ───────────────────────────────────────────
if dark:
    # Dark mode: single deep blue/indigo monochrome
    DK = "#1e2a3a"       # page bg
    DK_CARD = "#243447"  # card bg
    DK_BORDER = "#2e4460"
    DK_ACC = "#4a90d9"   # single accent colour (blue)
    DK_TEXT = "#d0dce8"
    DK_MUTED = "#7a9bb5"
    theme_css = f"""
    :root {{
      --bg:{DK}; --card:{DK_CARD}; --border:{DK_BORDER};
      --accent:{DK_ACC}; --text:{DK_TEXT}; --muted:{DK_MUTED};
    }}
    html,body,[class*="css"]{{background:var(--bg)!important;color:var(--text)!important;}}
    [data-testid="stSidebar"]{{background:#121e2b!important;border-right:2px solid {DK_BORDER}!important;}}
    [data-testid="stSidebar"] *{{color:{DK_TEXT}!important;}}
    [data-testid="stSidebar"] label{{color:{DK_MUTED}!important;font-size:.72rem!important;text-transform:uppercase;letter-spacing:.8px;}}
    [data-testid="stSidebar"] .stSelectbox>div>div,
    [data-testid="stSidebar"] .stTextInput input{{background:rgba(74,144,217,.1)!important;border:1px solid {DK_BORDER}!important;color:{DK_TEXT}!important;border-radius:8px!important;}}
    ::-webkit-scrollbar{{width:6px}}::-webkit-scrollbar-track{{background:{DK}}}
    ::-webkit-scrollbar-thumb{{background:{DK_BORDER};border-radius:4px}}
    """
    header_grad = f"linear-gradient(135deg,#0d1520,#121e2b,#1a2a3e)"
    header_border = DK_ACC
    logo_grad = f"linear-gradient(135deg,{DK_ACC},{DK_ACC}99)"
    header_title_color = DK_TEXT
    header_sub_color = DK_MUTED
    badge_bg = f"rgba(74,144,217,.2)"
    badge_border = f"rgba(74,144,217,.5)"
    badge_color = DK_ACC
    welcome_bg = DK
    welcome_h1_grad = f"linear-gradient(135deg,{DK_ACC},{DK_ACC}99)"
    welcome_sub = DK_MUTED
    welcome_box_bg = DK_CARD
    welcome_box_border = DK_BORDER
    welcome_box_text = DK_TEXT
    kpi_extra = f".kpi-card{{background:{DK_CARD}!important;border-color:{DK_BORDER}!important;}}.kpi-value{{color:{DK_TEXT}!important;}}"
    section_extra = f".section-card{{background:{DK_CARD}!important;border-color:{DK_BORDER}!important;}}"
    rest_extra = f".restaurant-card{{background:{DK_CARD}!important;border-color:{DK_BORDER}!important;}}"
    nores_extra = f".no-results{{background:{DK_CARD}!important;border-color:{DK_BORDER}!important;}}"
    # All kpi card tops: single blue
    kpi_tops = f"""
    .purple::before,.gold::before,.green::before,.orange::before,.pink::before,.teal::before{{
      background:linear-gradient(90deg,{DK_ACC},{DK_ACC}88)!important;
    }}"""
    PLOT_STYLE = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color=DK_MUTED,family="DM Sans"),
                      margin=dict(l=8,r=8,t=28,b=8),
                      xaxis=dict(gridcolor=DK_BORDER,linecolor=DK_CARD),
                      yaxis=dict(gridcolor=DK_BORDER,linecolor=DK_CARD))
    CHART_COLORS = [
        "rgba(74,144,217,1.0)",
        "rgba(74,144,217,0.85)",
        "rgba(74,144,217,0.70)",
        "rgba(74,144,217,0.55)",
        "rgba(74,144,217,0.45)",
        "rgba(74,144,217,0.35)",
        "rgba(74,144,217,0.25)",
        "rgba(74,144,217,0.15)",
    ]
    map_tiles = "CartoDB DarkMatter"
    footer_color = DK_MUTED
    toggle_label = "\u2600\ufe0f Switch to Light Mode"
    toggle_icon = "\U0001f319"
    app_bg = DK
    hr_color = DK_BORDER
    kpi_val_color = DK_TEXT
    mode_label = "\U0001f319 Dark Mode Active"
    src_btn_style = f"background:{DK_ACC};color:white;border:none;padding:6px 14px;border-radius:8px;font-weight:700;font-size:.8rem;cursor:pointer;"
else:
    theme_css = """
    :root {
      --bg:#fdf6ee; --card:#fff; --border:#f0e6d6;
      --accent:#c0392b; --text:#2c1810; --muted:#8d6e63;
    }
    html,body,[class*="css"]{{background:var(--bg)!important;color:var(--text)!important;}}
    [data-testid="stSidebar"]{{background:#a33c08!important;border-right:3px solid #7a2b06!important;}}
    [data-testid="stSidebar"] *{{color:#fdeee6!important;}}
    [data-testid="stSidebar"] label{{color:#f5c9ad!important;font-size:.72rem!important;text-transform:uppercase;letter-spacing:.8px;}}
    [data-testid="stSidebar"] .stSelectbox>div>div,
    [data-testid="stSidebar"] .stTextInput input{{background:rgba(255,255,255,.12)!important;border:1px solid rgba(255,255,255,.22)!important;color:#fdeee6!important;border-radius:8px!important;}}
    ::-webkit-scrollbar{{width:6px}}::-webkit-scrollbar-track{{background:#fdf6ee}}
    ::-webkit-scrollbar-thumb{{background:#d4a08a;border-radius:4px}}
    """
    header_grad = "linear-gradient(135deg,#2c1810,#6d2b1a,#922b21)"
    header_border = "#c0392b"
    logo_grad = "linear-gradient(135deg,#f39c12,#e67e22)"
    header_title_color = "#f5e6dc"
    header_sub_color = "#d4a08a"
    badge_bg = "rgba(243,156,18,.2)"
    badge_border = "rgba(243,156,18,.5)"
    badge_color = "#f39c12"
    welcome_bg = "#fdf6ee"
    welcome_h1_grad = "linear-gradient(135deg,#c0392b,#e67e22)"
    welcome_sub = "#8d6e63"
    welcome_box_bg = "linear-gradient(135deg,#fff8f3,#fff3e8)"
    welcome_box_border = "#f0c080"
    welcome_box_text = "#6d2b1a"
    kpi_extra = ""
    section_extra = ""
    rest_extra = ""
    nores_extra = ""
    kpi_tops = ""
    PLOT_STYLE = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#8d6e63",family="DM Sans"),
                      margin=dict(l=8,r=8,t=28,b=8),
                      xaxis=dict(gridcolor="#f0e6d6",linecolor="#d4a08a"),
                      yaxis=dict(gridcolor="#f0e6d6",linecolor="#d4a08a"))
    CHART_COLORS = ["#c0392b","#e67e22","#27ae60","#f39c12","#8e44ad","#16a085","#2980b9","#e91e8c"]
    map_tiles = "CartoDB Positron"
    footer_color = "#d4a08a"
    toggle_label = "\U0001f319 Switch to Dark Mode"
    toggle_icon = "\u2600\ufe0f"
    app_bg = "#fdf6ee"
    hr_color = "#f0e6d6"
    kpi_val_color = "#2c1810"
    mode_label = "\u2600\ufe0f Light Mode Active"
    src_btn_style = ""

PLOT_STYLE_GLOBAL = PLOT_STYLE
CHART_COLORS_GLOBAL = CHART_COLORS

# ── CSS ────────────────────────────────────────────────────────
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
{theme_css}
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif!important;}}
.main .block-container{{padding:0 2rem 3rem;max-width:1400px;}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes glow{{0%,100%{{box-shadow:0 0 10px rgba(74,144,217,.25)}}50%{{box-shadow:0 0 24px rgba(74,144,217,.55)}}}}
.header-bar{{background:{header_grad};border-bottom:3px solid {header_border};padding:16px 32px;
    margin:0 -2rem 28px;display:flex;align-items:center;justify-content:space-between;
    position:sticky;top:0;z-index:100;box-shadow:0 4px 20px rgba(0,0,0,.3);}}
.header-logo{{width:44px;height:44px;border-radius:12px;background:{logo_grad};display:flex;
    align-items:center;justify-content:center;font-size:1.3rem;animation:glow 3s ease-in-out infinite;}}
.live-badge{{background:{badge_bg};border:1px solid {badge_border};color:{badge_color};
    font-size:.7rem;font-weight:700;padding:4px 12px;border-radius:20px;}}
.kpi-card{{background:var(--card);border:1.5px solid var(--border);border-radius:16px;
    padding:18px 16px;position:relative;overflow:hidden;animation:fadeUp .5s ease both;
    transition:transform .22s,box-shadow .22s;box-shadow:0 2px 12px rgba(0,0,0,.07);}}
.kpi-card:hover{{transform:translateY(-4px);box-shadow:0 10px 30px rgba(74,144,217,.12);border-color:var(--accent);}}
.kpi-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:16px 16px 0 0;}}
.purple::before{{background:linear-gradient(90deg,#8e44ad,#3498db)}}
.gold::before{{background:linear-gradient(90deg,#f39c12,#e67e22)}}
.green::before{{background:linear-gradient(90deg,#27ae60,#16a085)}}
.orange::before{{background:linear-gradient(90deg,#e67e22,#e91e8c)}}
.pink::before{{background:linear-gradient(90deg,#e91e8c,#8e44ad)}}
.teal::before{{background:linear-gradient(90deg,#16a085,#27ae60)}}
{kpi_tops}
.kpi-value{{font-family:'Cormorant Garamond',serif;font-size:1.75rem;font-weight:700;line-height:1;color:var(--text);}}
.kpi-label{{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-top:5px;font-weight:600;}}
.section-card{{background:var(--card);border:1.5px solid var(--border);border-radius:18px;
    padding:22px;margin-bottom:18px;animation:fadeUp .55s ease both;box-shadow:0 2px 12px rgba(0,0,0,.07);}}
.section-title{{font-size:1rem;font-weight:700;display:flex;align-items:center;gap:9px;margin-bottom:16px;color:var(--text);}}
.dot{{width:9px;height:9px;border-radius:50%;display:inline-block;flex-shrink:0;}}
.restaurant-card{{background:var(--card);border:1.5px solid var(--border);border-radius:14px;
    padding:16px 20px;margin-bottom:10px;display:flex;align-items:center;gap:15px;
    animation:fadeUp .4s ease both;transition:border-color .22s,box-shadow .22s,transform .22s;
    box-shadow:0 2px 8px rgba(0,0,0,.07);}}
.restaurant-card:hover{{border-color:var(--accent);box-shadow:0 8px 28px rgba(74,144,217,.15);transform:translateY(-2px);}}
.rank-badge{{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#c0392b,#e67e22);
    display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1rem;color:white;flex-shrink:0;}}
.restaurant-name{{font-weight:700;font-size:.97rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text);}}
.restaurant-meta{{font-size:.76rem;color:var(--muted);margin-top:3px;}}
.tag{{display:inline-block;font-size:.64rem;font-weight:600;padding:3px 9px;border-radius:20px;margin-right:5px;margin-top:5px;}}
.tag-cuisine{{background:#f3e5f5;color:#7b1fa2}}.tag-region{{background:#fce4ec;color:#c2185b}}
.tag-delivery{{background:#e8f5e9;color:#2e7d32}}.tag-booking{{background:#e0f2f1;color:#00695c}}
.rating-box{{background:linear-gradient(135deg,#fff8e1,#fff3cd);border:1.5px solid #f9a825;
    border-radius:12px;padding:8px 13px;text-align:center;flex-shrink:0;}}
.rating-number{{font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:700;color:#e65100;line-height:1;}}
.rating-stars{{font-size:.58rem;color:#f9a825;margin-top:2px;}}
.maps-button{{display:inline-flex;align-items:center;gap:5px;background:linear-gradient(135deg,#27ae60,#2ecc71);
    color:white!important;text-decoration:none!important;font-size:.72rem;font-weight:700;padding:8px 14px;
    border-radius:9px;flex-shrink:0;white-space:nowrap;transition:opacity .18s,transform .18s;}}
.maps-button:hover{{opacity:.9;transform:scale(1.05);}}
.map-container{{border-radius:16px;overflow:hidden;border:2px solid var(--border);}}
.map-legend{{display:flex;gap:16px;flex-wrap:wrap;font-size:.76rem;color:var(--muted);margin-top:10px;}}
.legend-dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;}}
.no-results{{text-align:center;padding:48px 20px;border-radius:16px;border:2px dashed var(--border);background:var(--card);}}
.kpi-module-header{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700;
    color:var(--text);margin-bottom:6px;}}
.sentiment-bar-pos{{background:linear-gradient(90deg,#27ae60,#2ecc71);height:18px;border-radius:6px;transition:width .5s;}}
.sentiment-bar-neg{{background:linear-gradient(90deg,#c0392b,#e74c3c);height:18px;border-radius:6px;transition:width .5s;}}
.src-pill{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:.75rem;font-weight:700;margin-right:8px;cursor:pointer;border:2px solid transparent;transition:all .2s;}}
.src-active{{border-color:var(--accent);color:var(--accent);background:rgba(192,57,43,.08);}}
{kpi_extra}{section_extra}{rest_extra}{nores_extra}
hr{{border-color:{hr_color}!important;margin:22px 0!important;}}
</style>""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────
CITY_COORDS = {
    "Bangalore":(12.97,77.59),"Chennai":(13.08,80.27),"Delhi":(28.70,77.10),
    "New Delhi":(28.70,77.10),"Hyderabad":(17.38,78.48),"Kolkata":(22.57,88.36),
    "Mumbai":(19.07,72.87),"Pune":(18.52,73.85),"Tirupati":(13.62,79.41),
    "Vijayawada":(16.50,80.64),"Visakhapatnam":(17.68,83.21),"Vizag":(17.68,83.21),
    "Nellore":(14.45,79.98),"Kadapa":(14.47,78.82),"Guntur":(16.30,80.44),
    "Anantapur":(14.68,77.60),"Ahmedbad":(23.02,72.57),"Jaipur":(26.91,75.78),
    "Bhopal":(23.25,77.41),"Agra":(27.17,78.01),"Nashik":(19.99,73.78),
    "Imphal":(24.81,93.93),"surat":(21.17,72.83),"Bhimavaram":(16.54,81.52),
    "Venkatagiri":(13.96,79.58),"kurnool":(15.83,78.04),"chittoor":(13.21,79.10),
}

# ── Column auto-detect ─────────────────────────────────────────
def detect_columns(df):
    cmap = {c.lower().strip(): c for c in df.columns}
    def find(*names):
        for n in names:
            if n.lower() in cmap: return cmap[n.lower()]
        return None
    return {
        "name":     find("name","restaurant name","restaurant_name","title"),
        "city":     find("city","location","town","area"),
        "cuisine":  find("cuisines","cuisine","food type","category","type"),
        "rating":   find("rating","aggregate_rating","rate","avg rating","score"),
        "votes":    find("votes","num_votes","reviews","review_count","total votes"),
        "cost":     find("cost for two","cost_for_two","approx_cost(for_two_people)","average cost","price for two","price"),
        "delivery": find("online delivery","has_online_delivery","delivery"),
        "booking":  find("table booking","has_table_booking","book table"),
        "region":   find("region","zone","district"),
        "maps":     find("google maps url","maps url","google maps","map url"),
        "menu":     find("food items","dish_liked","dishes","menu","items","popular dishes","menu items"),
    }

# ── Helpers ────────────────────────────────────────────────────
def make_stars(r):
    f = min(int(float(r)),5)
    return "\u2605"*f + "\u2606"*(5-f)

def get_maps_url(name, city, raw):
    if str(raw).startswith("http"): return raw
    return f"https://www.google.com/maps/search/?api=1&query={str(name).replace(' ','+')}+{city}"

def get_city_maps_url(city):
    coords = CITY_COORDS.get(city)
    if coords:
        lat,lon = coords
        return f"https://www.google.com/maps/search/restaurants/@{lat},{lon},13z"
    return f"https://www.google.com/maps/search/?api=1&query=restaurants+in+{city.replace(' ','+')}"

def sentiment_score(rating):
    """Simple rule: >=4.0 positive, <4.0 negative."""
    return "positive" if float(rating)>=4.0 else "negative"

@st.cache_data(show_spinner="Loading dataset\u2026")
def load_uploaded(file):
    df = pd.read_excel(file,engine="openpyxl") if file.name.endswith(("xlsx","xls")) else pd.read_csv(file,encoding="latin1")
    df.columns = [c.strip() for c in df.columns]
    c = detect_columns(df)
    for key in ["rating","votes","cost"]:
        if c[key]:
            df[c[key]] = pd.to_numeric(df[c[key]],errors="coerce")
            df[c[key]] = df[c[key]].fillna(df[c[key]].median())
    for key in ["name","city","cuisine","delivery","booking","region","maps","menu"]:
        if c[key]:
            df[c[key]] = df[c[key]].astype(str).str.strip()
    return df

@st.cache_data(show_spinner=False)
def load_default():
    df = pd.read_csv(io.StringIO(DEFAULT_CSV))
    df.columns = [c.strip() for c in df.columns]
    return df

# ── Load data based on source ─────────────────────────────────
src = st.session_state.data_src   # "default" or "upload"

if src == "default":
    df = load_default()
else:
    df = st.session_state.df if st.session_state.df is not None else pd.DataFrame()

col = detect_columns(df) if not df.empty else {k:None for k in
      ["name","city","cuisine","rating","votes","cost","delivery","booking","region","maps","menu"]}

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='padding:10px 0;text-align:center;'><div style='font-size:1.8rem'>\U0001f4c2</div>"
                "<div style='font-weight:700;font-size:1rem;margin-top:4px;'>Data Source</div></div>",
                unsafe_allow_html=True)

    # ── Data source selector ───────────────────────────────────
    st.markdown("<div style='font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>\U0001f4ca Choose Dataset</div>",
                unsafe_allow_html=True)
    src_choice = st.radio("", ["\U0001f3e0 Default Dataset (Built-in)", "\U0001f4c1 Upload My Dataset"],
                          index=0 if src=="default" else 1, label_visibility="collapsed")
    if "Default" in src_choice:
        if st.session_state.data_src != "default":
            st.session_state.data_src = "default"
            st.rerun()
    else:
        if st.session_state.data_src != "upload":
            st.session_state.data_src = "upload"
            st.rerun()

    if src == "upload":
        st.markdown("---")
        file = st.file_uploader("Upload CSV / Excel", type=["xlsx","xls","csv"], label_visibility="collapsed")
        if file:
            fid = file.name + str(file.size)
            if st.session_state.get("fid") != fid:
                st.session_state.df = load_uploaded(file)
                st.session_state.fid = fid
                st.rerun()
        if df.empty:
            st.info("Upload a file to begin.")

    # ── Dark / Light Mode ──────────────────────────────────────
    st.markdown("---")
    st.markdown(f"<div style='text-align:center;font-weight:700;font-size:.85rem;margin-bottom:8px;'>{toggle_icon} Appearance</div>",
                unsafe_allow_html=True)
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align:center;font-weight:700;font-size:1rem;margin-bottom:12px;'>\U0001f50d Filters</div>",
                unsafe_allow_html=True)

    if not df.empty:
        sel_city = "All"
        if col["city"]:
            st.markdown("<span style='font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#f39c12;'>\U0001f3d9\ufe0f Filter by City</span>", unsafe_allow_html=True)
            sel_city = st.selectbox("", ["All"]+sorted(df[col["city"]].dropna().unique().tolist()), key="city", label_visibility="collapsed")
        sel_cuisine = "All"
        if col["cuisine"]:
            st.markdown("<span style='font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#2ecc71;'>\U0001f35c Filter by Cuisine</span>", unsafe_allow_html=True)
            sel_cuisine = st.selectbox("", ["All"]+sorted(df[col["cuisine"]].dropna().unique().tolist()), key="cuisine", label_visibility="collapsed")
        st.markdown("---")
        sel_region = st.selectbox("\U0001f4cc Region",["All"]+sorted(df[col["region"]].dropna().unique().tolist())) if col["region"] else "All"
        search   = st.text_input("\U0001f50e Search by Name", placeholder="Type name\u2026")
        min_r    = st.slider("\u2b50 Min Rating", float(df[col["rating"]].min()), float(df[col["rating"]].max()), float(df[col["rating"]].min()), 0.1) if col["rating"] else 0.0
        max_c    = st.slider("\U0001f4b0 Max Cost (\u20b9)", 0, int(df[col["cost"]].max()), int(df[col["cost"]].max()), 100) if col["cost"] else 999999
        min_v    = st.number_input("\U0001f5f3\ufe0f Min Votes", min_value=0, value=0, step=50)
        top_n    = st.slider("\U0001f3c6 Top N", 5, 30, 10)
        st.markdown("---")
        del_only = st.checkbox("\U0001f6f5 Online Delivery Only")
        bk_only  = st.checkbox("\U0001f4c5 Table Booking Only")
    else:
        sel_city=sel_cuisine=sel_region="All"
        search=""; min_r=0.0; max_c=999999; min_v=0; top_n=10; del_only=bk_only=False

# ── Apply filters ──────────────────────────────────────────────
fdf = df.copy()
if not df.empty:
    if sel_city    != "All" and col["city"]:    fdf = fdf[fdf[col["city"]]    == sel_city]
    if sel_cuisine != "All" and col["cuisine"]: fdf = fdf[fdf[col["cuisine"]].str.contains(sel_cuisine,case=False,na=False)]
    if sel_region  != "All" and col["region"]:  fdf = fdf[fdf[col["region"]]  == sel_region]
    if search      and col["name"]:             fdf = fdf[fdf[col["name"]].str.contains(search,case=False,na=False)]
    if col["rating"]:   fdf = fdf[fdf[col["rating"]]  >= min_r]
    if col["cost"]:     fdf = fdf[fdf[col["cost"]]    <= max_c]
    if col["votes"]:    fdf = fdf[fdf[col["votes"]]   >= min_v]
    if del_only and col["delivery"]: fdf = fdf[fdf[col["delivery"]].str.lower()=="yes"]
    if bk_only  and col["booking"]:  fdf = fdf[fdf[col["booking"]].str.lower() =="yes"]

# ── Welcome screen (upload mode, no file yet) ─────────────────
if df.empty:
    st.markdown(f"<style>.stApp{{background-color:{welcome_bg}!important;}}</style>", unsafe_allow_html=True)
    st.markdown(f"""<div style="min-height:80vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
        <div style="font-size:5rem;margin-bottom:20px;">\U0001f37d\ufe0f</div>
        <h1 style="font-family:'Cormorant Garamond',serif;font-size:3rem;background:{welcome_h1_grad};-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:10px;">Restaurant Analytics Dashboard</h1>
        <p style="font-size:1.1rem;color:{welcome_sub};margin-bottom:30px;max-width:560px;line-height:1.7;">Upload your restaurant CSV/Excel or switch to the Default Dataset.</p>
        <div style="background:{welcome_box_bg};border:2px solid {welcome_box_border};padding:18px 36px;border-radius:16px;">
            <p style="color:{welcome_box_text};font-size:1rem;margin:0;font-weight:500;">\U0001f448 Use the <b>Sidebar</b> to select Default Dataset or upload your own.</p>
        </div></div>""", unsafe_allow_html=True)
    st.stop()

# ── Header ─────────────────────────────────────────────────────
st.markdown(f"<style>.stApp{{background-color:{app_bg}!important;}}</style>", unsafe_allow_html=True)
src_label = "\U0001f3e0 Default Dataset" if src=="default" else f"\U0001f4c1 {st.session_state.get('fid','').split('.csv')[0][:25]}"
st.markdown(f"""<div class='header-bar'>
    <div style='display:flex;align-items:center;gap:14px;'>
        <div class='header-logo'>\U0001f37d\ufe0f</div>
        <div>
            <div style='font-weight:800;font-size:1.1rem;color:{header_title_color};'>\U0001f1ee\U0001f1f3 Restaurant Analytics</div>
            <div style='font-size:.72rem;color:{header_sub_color};margin-top:2px;'>Final Year Project Dashboard &nbsp;·&nbsp; {src_label}</div>
        </div>
    </div>
    <div style='display:flex;align-items:center;gap:14px;'>
        <span style='font-size:.75rem;color:{header_sub_color};'>{mode_label}</span>
        <span class='live-badge'>\u2736 Live Dashboard</span>
    </div></div>""", unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center;color:var(--muted);font-size:.85rem;margin-top:-10px;margin-bottom:28px;'>"
            f"Dataset: {len(df):,} records \u00b7 {len(df.columns)} columns \u00b7 Showing {len(fdf):,} after filters</p>",
            unsafe_allow_html=True)

# ── KPI SUMMARY ROW ────────────────────────────────────────────
avg_r   = fdf[col["rating"]].mean()           if col["rating"]  and not fdf.empty else 0
avg_c   = fdf[col["cost"]].mean()             if col["cost"]    and not fdf.empty else 0
top_cui = fdf[col["cuisine"]].mode()[0][:14]  if col["cuisine"] and not fdf.empty else "\u2014"
n_city  = fdf[col["city"]].nunique()          if col["city"]    and not fdf.empty else 0

kpi_list = [("purple","\U0001f37d\ufe0f",f"{len(fdf):,}","Total Restaurants"),
            ("gold","\u2b50",f"{avg_r:.2f}","Avg Rating"),
            ("green","\U0001f947",top_cui,"Top Cuisine"),
            ("orange","\U0001f4b0",f"\u20b9{avg_c:.0f}","Avg Cost (2)"),
            ("pink","\U0001f3d9\ufe0f",str(n_city),"Cities"),
            ("teal","\U0001f4ca",str(len(df.columns)),"Total Columns")]
for kc,(color,icon,val,lbl) in zip(st.columns(6),kpi_list):
    kc.markdown(f"<div class='kpi-card {color}'><div style='font-size:1.5rem;margin-bottom:6px;'>{icon}</div>"
                f"<div class='kpi-value'>{val}</div><div class='kpi-label'>{lbl}</div></div>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ── KPI ANALYTICS MODULE ─────────────────────────────────────
# ══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""<div class='section-card'>
  <div class='section-title'><span class='dot' style='background:var(--accent);'></span>
  \U0001f4ca KPI Analytics Module
  <span style='font-size:.72rem;font-weight:400;color:var(--muted);margin-left:6px;'>
    Deep metrics for the filtered selection</span></div>""", unsafe_allow_html=True)

# city selector inside the KPI module
kpi_cities = ["All (Filtered)"] + (sorted(fdf[col["city"]].dropna().unique().tolist()) if col["city"] and not fdf.empty else [])
kpi_city = st.selectbox("\U0001f3d9\ufe0f Select City for KPI Module", kpi_cities, key="kpi_city")
kdf = fdf.copy()
if kpi_city != "All (Filtered)" and col["city"]:
    kdf = kdf[kdf[col["city"]] == kpi_city]

st.markdown("</div>", unsafe_allow_html=True)

# ── KPI metric row ─────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
k_avg_r  = kdf[col["rating"]].mean()     if col["rating"]  and not kdf.empty else 0
k_total  = len(kdf)
k_top_c  = kdf[col["cuisine"]].mode()[0] if col["cuisine"] and not kdf.empty else "\u2014"
k_avg_cp = kdf[col["cost"]].mean()       if col["cost"]    and not kdf.empty else 0
k_pos    = int((kdf[col["rating"]] >= 4.0).sum()) if col["rating"] and not kdf.empty else 0
k_neg    = int((kdf[col["rating"]] <  4.0).sum()) if col["rating"] and not kdf.empty else 0
k_sent   = f"\U0001f7e2 {k_pos} / \U0001f534 {k_neg}"

for kc,(icon,val,lbl) in zip([k1,k2,k3,k4,k5],[
    ("\u2b50", f"{k_avg_r:.2f}", "Avg Rating"),
    ("\U0001f37d\ufe0f", f"{k_total:,}", "Total Restaurants"),
    ("\U0001f947", k_top_c[:16], "Most Popular Cuisine"),
    ("\U0001f4b0", f"\u20b9{k_avg_cp:.0f}", "Avg Price Range"),
    ("\U0001f4dd", k_sent, "\U0001f7e2 Pos / \U0001f534 Neg Reviews"),
]):
    kc.markdown(f"<div class='kpi-card green'>"
                f"<div style='font-size:1.4rem;margin-bottom:6px;'>{icon}</div>"
                f"<div class='kpi-value' style='font-size:1.4rem;'>{val}</div>"
                f"<div class='kpi-label'>{lbl}</div></div>",
                unsafe_allow_html=True)

# ── Sentiment breakdown bar ────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if not kdf.empty and col["rating"] and k_total > 0:
    pos_pct = k_pos / k_total * 100
    neg_pct = 100 - pos_pct
    city_lbl = kpi_city if kpi_city != "All (Filtered)" else "All Selected Cities"
    st.markdown(f"""<div class='section-card'>
      <div class='section-title'><span class='dot' style='background:#27ae60;'></span>
      \U0001f4dd Review Sentiment Analysis &mdash; {city_lbl}</div>
      <div style='margin-bottom:8px;font-size:.85rem;color:var(--muted);'>
        Based on rating threshold: \u2265 4.0 = Positive, &lt; 4.0 = Negative</div>
      <div style='display:flex;gap:12px;align-items:center;margin-bottom:10px;'>
        <span style='font-size:.8rem;color:#27ae60;font-weight:700;min-width:90px;'>\U0001f7e2 Positive</span>
        <div style='flex:1;background:rgba(0,0,0,.08);border-radius:6px;overflow:hidden;'>
          <div class='sentiment-bar-pos' style='width:{pos_pct:.1f}%'></div>
        </div>
        <span style='font-size:.85rem;font-weight:700;color:#27ae60;min-width:70px;text-align:right;'>{k_pos} ({pos_pct:.1f}%)</span>
      </div>
      <div style='display:flex;gap:12px;align-items:center;'>
        <span style='font-size:.8rem;color:#c0392b;font-weight:700;min-width:90px;'>\U0001f534 Negative</span>
        <div style='flex:1;background:rgba(0,0,0,.08);border-radius:6px;overflow:hidden;'>
          <div class='sentiment-bar-neg' style='width:{neg_pct:.1f}%'></div>
        </div>
        <span style='font-size:.85rem;font-weight:700;color:#c0392b;min-width:70px;text-align:right;'>{k_neg} ({neg_pct:.1f}%)</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ── City-wise sentiment table ──────────────────────────────────
if not fdf.empty and col["rating"] and col["city"]:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#4a90d9;'></span>\U0001f3d9\ufe0f City-wise Sentiment Breakdown</div>",
                unsafe_allow_html=True)
    city_sent = fdf.groupby(col["city"]).agg(
        Total   =(col["name"] if col["name"] else col["city"], "count"),
        AvgRating=(col["rating"],"mean"),
        Positive =(col["rating"], lambda x: (x>=4.0).sum()),
        Negative =(col["rating"], lambda x: (x<4.0).sum()),
    ).reset_index()
    city_sent.columns = ["City","Total","Avg Rating","\U0001f7e2 Positive","\U0001f534 Negative"]
    city_sent["Avg Rating"] = city_sent["Avg Rating"].round(2)
    city_sent["% Positive"] = (city_sent["\U0001f7e2 Positive"] / city_sent["Total"] * 100).round(1).astype(str) + "%"
    city_sent = city_sent.sort_values("Total", ascending=False)
    st.dataframe(city_sent, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ── TOP N RESTAURANTS ─────────────────────────────────────────
# ════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
active = " \u00b7 ".join(x for x in [f"\U0001f3d9\ufe0f {sel_city}" if sel_city!="All" else "",
                                  f"\U0001f35c {sel_cuisine}" if sel_cuisine!="All" else ""] if x) or "No active filters"
st.markdown(f"<div class='section-card'><div class='section-title'><span class='dot' style='background:#c0392b;'></span>"
            f"\U0001f3c6 Top {top_n} Restaurants <span style='font-size:.72rem;font-weight:400;color:var(--muted);margin-left:6px;'>{active}</span></div></div>",
            unsafe_allow_html=True)

if fdf.empty:
    st.markdown("<div class='no-results'><div style='font-size:2.5rem'>\U0001f50d</div>"
                "<div style='font-size:1rem;color:var(--muted);font-weight:600;margin-top:8px;'>No restaurants match your filters.</div></div>",
                unsafe_allow_html=True)
else:
    name_col  = col["name"] or df.columns[0]
    sort_cols = [c for c in [col["rating"],col["votes"]] if c]
    top_df    = (fdf.sort_values(sort_cols,ascending=[False]*len(sort_cols)) if sort_cols else fdf)
    top_df    = top_df.drop_duplicates(subset=[name_col]).head(top_n).reset_index(drop=True)

    for idx,row in top_df.iterrows():
        def g(key,default=""):
            return str(row.get(col[key],default)) if col[key] else str(default)
        name     = g("name",f"Restaurant {idx+1}")
        city     = g("city"); region=g("region"); cuisine=g("cuisine")
        delivery = g("delivery","No"); booking=g("booking","No")
        rating   = float(row.get(col["rating"],0)) if col["rating"] else 0
        votes    = int(row.get(col["votes"],0))   if col["votes"]  else 0
        cost     = int(row.get(col["cost"],0))    if col["cost"]   else 0
        murl     = get_maps_url(name,city,g("maps"))

        tags  = f"<span class='tag tag-cuisine'>\U0001f35c {cuisine}</span>" if cuisine not in ["","nan"] else ""
        tags += f"<span class='tag tag-region'>\U0001f4cc {region}</span>"   if region  not in ["","nan"] else ""
        tags += "<span class='tag tag-delivery'>\U0001f6f5 Delivery</span>"    if delivery.lower()=="yes" else ""
        tags += "<span class='tag tag-booking'>\U0001f4c5 Booking</span>"      if booking.lower() =="yes" else ""

        st.markdown(f"""<div class='restaurant-card'>
            <div class='rank-badge'>{idx+1}</div>
            <div style='flex:1;min-width:0;'>
                <div class='restaurant-name'>{name}</div>
                <div class='restaurant-meta'>\U0001f4cd {city} &nbsp;\u00b7&nbsp; \U0001f4b0 \u20b9{cost} for two &nbsp;\u00b7&nbsp; \U0001f5f3\ufe0f {votes:,} votes</div>
                <div style='margin-top:3px;'>{tags}</div>
            </div>
            <div style='display:flex;align-items:center;gap:10px;flex-shrink:0;'>
                <div class='rating-box'>
                    <div class='rating-number'>{rating:.1f}</div>
                    <div class='rating-stars'>{make_stars(rating)}</div>
                </div>
                <a href='{murl}' target='_blank' class='maps-button'>\U0001f5fa\ufe0f Maps</a>
            </div></div>""", unsafe_allow_html=True)

# ── Charts row 1 ───────────────────────────────────────────────
c1,c2 = st.columns(2)
with c1:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#e67e22;'></span>Restaurants by City</div>", unsafe_allow_html=True)
    if col["city"] and not fdf.empty:
        d = fdf[col["city"]].value_counts().reset_index(); d.columns=["City","Count"]
        fig = px.bar(d,x="City",y="Count",color="Count",color_continuous_scale=[[0,"#fff3e0"],[1,"#c0392b"]])
        fig.update_layout(**PLOT_STYLE_GLOBAL,coloraxis_showscale=False); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#27ae60;'></span>Cuisine Distribution</div>", unsafe_allow_html=True)
    if col["cuisine"] and not fdf.empty:
        d = fdf[col["cuisine"]].value_counts().reset_index(); d.columns=["Cuisine","Count"]
        fig = px.pie(d,values="Count",names="Cuisine",hole=0.45,color_discrete_sequence=CHART_COLORS_GLOBAL)
        fig.update_layout(**PLOT_STYLE_GLOBAL,showlegend=True,legend=dict(font=dict(color="grey",size=11)))
        fig.update_traces(textfont_color="#2c1810",pull=[0.02]*len(d)); st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Charts row 2 ───────────────────────────────────────────────
c3,c4 = st.columns(2)
with c3:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#f39c12;'></span>Rating Distribution</div>", unsafe_allow_html=True)
    if col["rating"] and not fdf.empty:
        fig = px.histogram(fdf,x=col["rating"],nbins=15,color_discrete_sequence=["#f39c12"])
        fig.update_layout(**PLOT_STYLE_GLOBAL); fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#e91e8c;'></span>Price Distribution</div>", unsafe_allow_html=True)
    if col["cost"] and not fdf.empty:
        fig = px.histogram(fdf,x=col["cost"],nbins=20,color_discrete_sequence=["#e91e8c"])
        fig.update_layout(**PLOT_STYLE_GLOBAL); fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Charts row 3 ───────────────────────────────────────────────
c5,c6 = st.columns(2)
with c5:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#e91e8c;'></span>Regional Distribution</div>", unsafe_allow_html=True)
    if col["region"] and not fdf.empty:
        d = fdf[col["region"]].value_counts().reset_index(); d.columns=["Region","Count"]
        fig = px.bar(d,x="Region",y="Count",color="Region",color_discrete_sequence=CHART_COLORS_GLOBAL)
        fig.update_layout(**PLOT_STYLE_GLOBAL,showlegend=False); fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c6:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#16a085;'></span>Delivery vs Table Booking</div>", unsafe_allow_html=True)
    if not fdf.empty and col["delivery"] and col["booking"]:
        dy = int((fdf[col["delivery"]].str.lower()=="yes").sum())
        by = int((fdf[col["booking"]].str.lower() =="yes").sum())
        fig = go.Figure([go.Bar(name="Online Delivery",x=["Yes","No"],y=[dy,len(fdf)-dy],marker_color=["#27ae60","#f0e6d6"]),
                         go.Bar(name="Table Booking",  x=["Yes","No"],y=[by,len(fdf)-by],marker_color=["#16a085","#f0e6d6"])])
        fig.update_layout(**PLOT_STYLE_GLOBAL,barmode="group",showlegend=True,legend=dict(font=dict(color="grey",size=11)))
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Folium map ─────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='section-title' style='margin-left:4px;'><span class='dot' style='background:#27ae60;'></span>\U0001f5fa\ufe0f Restaurant Location Map</div>",
            unsafe_allow_html=True)
st.caption("Click any marker to see city stats and open Google Maps.")

if not fdf.empty and col["city"] and col["name"]:
    agg_dict = {"Count":(col["name"],"count"),"Top":(col["name"],"first")}
    if col["rating"]: agg_dict["AvgR"]=(col["rating"],"mean")
    city_agg = fdf.groupby(col["city"]).agg(**agg_dict).reset_index()
    city_agg.columns = ["City"]+list(agg_dict.keys())
    if "AvgR" not in city_agg.columns: city_agg["AvgR"]=4.0

    m = folium.Map(location=[20.59,78.96],zoom_start=5,tiles=map_tiles)
    for _,r in city_agg.iterrows():
        lat,lon = CITY_COORDS.get(r["City"],(20.5,79.0))
        ar = float(r["AvgR"])
        curl = get_city_maps_url(r["City"])
        color = "#27ae60" if ar>=4.3 else ("#f39c12" if ar>=4.0 else "#c0392b")
        popup_bg = "#243447" if dark else "#fff8f3"
        popup_tc = "#d0dce8" if dark else "#2c1810"
        popup_bd = "#2e4460" if dark else "#f0c080"
        popup = (f"<div style='font-family:DM Sans,sans-serif;background:{popup_bg};color:{popup_tc};"
                 f"padding:12px 16px;border-radius:12px;min-width:190px;border:1.5px solid {popup_bd};'>"
                 f"<b style='color:#c0392b;'>{r['City']}</b><br>"
                 f"<span style='color:#8d6e63;font-size:.75rem;'>\U0001f37d\ufe0f {int(r['Count'])} restaurants</span><br>"
                 f"<span style='color:#e67e22;font-size:.75rem;'>\u2b50 Avg {ar:.2f}</span><br>"
                 f"<span style='color:#8d6e63;font-size:.72rem;'>Top: {str(r['Top'])[:28]}</span><br><br>"
                 f"<a href='{curl}' target='_blank' style='background:linear-gradient(135deg,#27ae60,#2ecc71);"
                 f"color:white;text-decoration:none;padding:5px 12px;border-radius:8px;font-size:.72rem;font-weight:700;'>\U0001f5fa\ufe0f Open Google Maps</a></div>")
        folium.CircleMarker(location=[lat,lon],radius=8+min(int(r["Count"])//10,12),
                            color=color,fill=True,fill_color=color,fill_opacity=0.82,
                            popup=folium.Popup(popup,max_width=240),
                            tooltip=f"\U0001f4cd {r['City']} \u00b7 {int(r['Count'])} restaurants \u00b7 \u2b50{ar:.1f}").add_to(m)
    st.markdown("<div class='map-container'>", unsafe_allow_html=True)
    st_folium(m,width="100%",height=480)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='map-legend'>"
                "<span><span class='legend-dot' style='background:#27ae60'></span>\u2265 4.3 Excellent</span>"
                "<span><span class='legend-dot' style='background:#f39c12'></span>4.0\u20134.3 Good</span>"
                "<span><span class='legend-dot' style='background:#c0392b'></span>&lt;4.0 Average</span>"
                "<span style='color:var(--muted);'>\u00b7 Marker size = restaurant count</span></div>",
                unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown(f"<div style='text-align:center;color:{footer_color};font-size:.75rem;padding:22px 0 8px;font-weight:500;'>"
            "\U0001f1ee\U0001f1f3 Restaurant Analytics Dashboard \u00b7 Built with Streamlit &amp; Plotly \u00b7 Final Year Project"
            "</div>", unsafe_allow_html=True)
