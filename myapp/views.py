from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SimpleSignupForm, TransactionForm
from .models import Transaction
import requests
from datetime import datetime
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from django.contrib.auth import logout


# Alpha Vantage API key for stock data retrieval
API_KEY = '61PFNDE6RZ9LDM26'

# Function to fetch stock data using Alpha Vantage API
def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        return {'error': 'Invalid stock symbol or no data available from API.'}

    time_series = data["Time Series (Daily)"]
    sorted_dates = sorted(time_series.keys(), reverse=True)[:10]

    dates = []
    prices = []
    for date in sorted_dates:
        # Convert date to UNIX timestamp for Highcharts
        dates.append(int(datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000))
        prices.append(float(time_series[date]["4. close"]))

    return {
        'symbol': symbol,
        'dates': dates,
        'prices': prices
    }

# Generate a professional trading-style graph for static usage
def generate_graph(dates, prices):
    plt.style.use('dark_background')  # Use a dark background for a trading-style look
    fig, ax = plt.subplots(figsize=(12, 6))

    # Convert dates for plotting
    dates = pd.to_datetime(dates, unit='ms')

    # Plot data with trading-style formatting
    ax.plot(dates, prices, color="#1f77b4", marker="o", markersize=5, markerfacecolor="#ff7f0e", linewidth=2)

    # Customize the grid and background
    ax.grid(visible=True, color="white", linestyle="--", linewidth=0.5, alpha=0.3)
    ax.set_facecolor("#1e1e1e")
    fig.patch.set_facecolor("#1e1e1e")

    # Formatting x-axis with dates and rotation
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45, color="white")
    plt.yticks(color="white")

    # Labels and title with professional styling
    ax.set_title("Stock Prices Over Last 10 Days", fontsize=16, fontweight="bold", color="white")
    ax.set_xlabel("Date", fontsize=12, color="white")
    ax.set_ylabel("Closing Price (USD)", fontsize=12, color="white")

    # Additional styling to hide unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("gray")
    ax.spines["bottom"].set_color("gray")

    # Save plot to a BytesIO object to pass to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return graph_base64

# Signup view
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('stock')  # Redirect authenticated users to the stock page

    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after sign up
            return render(request, 'signup_confirmation.html')  # Show confirmation page
    else:
        form = SimpleSignupForm()

    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('stock')  # Redirect to stock page if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in after successful authentication
                return redirect('stock')  # Redirect to stock page after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)  # This logs the user out
    return redirect('login')  # Redirect to login page after logout

# Portfolio view with transaction history and buy/sell functionality
@login_required
def portfolio_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('portfolio')  # Redirect after saving
    return render(request, 'portfolio.html', {'transactions': transactions, 'form': form})

# Main stock view to handle stock data lookup and profit calculation
@login_required
def stock_view(request):
    context = {
        'dates': [],  # Default empty list for dates
        'prices': [],  # Default empty list for prices
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        # Handle stock lookup form
        if action == 'stock_lookup':
            stock_name_or_symbol = request.POST.get('stock_symbol')
            if stock_name_or_symbol:
                stock_name_or_symbol = stock_name_or_symbol.strip()
                stock_data = get_stock_data(stock_name_or_symbol)

                if 'error' in stock_data:
                    context['error'] = stock_data['error']
                else:
                    graph_image = generate_graph(stock_data['dates'], stock_data['prices'])
                    context.update({
                        'symbol': stock_data['symbol'],
                        'current_price': stock_data['prices'][0],
                        'graph_image': graph_image,
                        'dates': stock_data['dates'],
                        'prices': stock_data['prices'],
                    })

        # Handle profit calculator form
        elif action == 'profit_calculator':
            try:
                symbol = request.POST.get('symbol')
                current_price = float(request.POST.get('current_price'))
                buy_price = float(request.POST.get('buy_price'))
                sell_price = float(request.POST.get('sell_price'))
                shares = int(request.POST.get('shares'))

                # Rebuild stock data context to maintain stock info
                dates = request.POST.getlist('dates[]')
                prices = request.POST.getlist('prices[]')

                # Calculate profit
                profit = (sell_price - buy_price) * shares
                context.update({
                    'symbol': symbol,
                    'current_price': current_price,
                    'profit': profit,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'shares': shares,
                    'dates': dates,
                    'prices': prices,
                    'graph_image': generate_graph(dates, prices)
                })
            except ValueError:
                context['error'] = "Invalid input for the profit calculator. Please enter valid numbers."

    return render(request, 'stock_price.html', context)
