
Stock Market Tracker Application - README
Introduction
The Stock Market Tracker Application is a Django-based web application designed to help users monitor stock prices, calculate profits from trades, and manage a portfolio of transactions. It uses the Alpha Vantage API to retrieve stock data and provides an interactive user interface for stock lookup and profit calculation.

Features
User Authentication: Secure signup, login, and logout functionalities.
Stock Lookup: Fetch stock data for the last 10 days using the Alpha Vantage API and display it with a professional-style graph.
Profit Calculator: Calculate profits based on buying/selling price and the number of shares.
Portfolio Management: Add and track transactions in the user portfolio (buy/sell).
Interactive Graphs: Visualize stock prices with an aesthetically pleasing and professional design.
Prerequisites
Python 3.7 or higher
Django 4.0 or higher
Alpha Vantage API Key (replace API_KEY in the code with your key)
Libraries:
matplotlib
pandas
requests
datetime
