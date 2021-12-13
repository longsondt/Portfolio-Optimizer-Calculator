pip install PyPortfolioOpt
pip install yfinance
pip install pandas
pip install pandas-datareader

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import yfinance as yf
import datetime as datetime
from pypfopt import expected_returns, risk_models, objective_functions
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

"""# Step 1. Ask for the available fund, number of securities to be invested and their names"""

def get_total_portfolio_value():
  """
  Asks the user for the total number of money (FLOAT) (USD) that 
  they want to invest in the portfolio. Handles any 
  misinput from the users. Returns a FLOAT
  """

  while True: 
    try:
      total_portfolio_value = float(input('How much (in USD) will you invest'\
                                          ' in this portfolio? '))
    except ValueError:
      print('Please enter a number and not words')
      continue
    if total_portfolio_value < 0:
      print('You cannot invest with negative fund...')
    else: 
      break

  return total_portfolio_value

def get_number_of_securities():
  """
  Asks the user for the total number (INT) of companies that they 
  want to include in the portfolio. It will handle any misinput from the users.
  Returns an INT
  """

  while True:
    try: 
      number_of_securities = int(input('How many different companies will you'\
                                       ' invest in this portfolio? '))
    except ValueError:
      print('Please enter a number and not words')
      continue
    if number_of_securities < 0:
      print('You cannot have negative number of securities...')
    else: 
      break
  return number_of_securities

def get_securities(number_of_securities):
  """
  Accepts a (LIST) number of securities, then ask the user for the ticker 
  symbols of those securities. It will handle any misinput from the users.
  Returns a LIST of securities
  """
  securities = []

  for number in range(number_of_securities):
    while True:
      try:
          security = input(f'Please type in security {number+1}: ').upper()
          ticker = yf.Ticker(security)
          ticker_check = ticker.info['longBusinessSummary']
          break
      except KeyError:
          print("Please enter a valid ticker symbol")
    securities.append(security)

  return securities


total_portfolio_value = get_total_portfolio_value()
number_of_securities = get_number_of_securities()
securities = get_securities(number_of_securities)

"""# Step 2. Get the start and end interval for historical price data

## 2.1 Get the start of the period
"""

print('\n--- Creating starting period ---')

def get_start_period():
  """
  Asks the users the year, month, and date (INT) and convert it into 
  datetime format. Handles any misinput from the users.
  Returns a datetime object
  """

  while True: 
    try:
      start_year = int(input('Please enter the start year: '))
    except ValueError: 
      print('Please do not enter words')
      continue
    if start_year < 0:
      print('You cannot have a negative year...')
      continue
    elif len(str(start_year)) != 4:
      print("Please enter the year in the correct format. For example '2001'")
      continue
    else: 
      break 

  while True: 
    try:
      start_month = int(input('Please enter the start month: '))
    except ValueError: 
      print('Please do not enter words')
      continue
    if start_month < 0:
      print('You cannot have a negative year...')
      continue
    elif len(str(start_month)) > 2:
      print("Please enter the month in the correct format. For example '2' or 12")
      continue
    else: 
      break 

  while True: 
    try:
      start_date = int(input('Please enter the start date: '))
    except ValueError: 
      print('Please do not enter words')
      continue
    if start_date < 0:
      print('You cannot have a negative date...')
      continue
    elif len(str(start_date)) > 2:
      print("Please enter the date in the correct format. For example '2' or 12")
      continue
    else: 
      break 

  start_date = datetime.date(start_year, start_month, start_date)

  return start_date


start_date = get_start_period()

"""## 2.2 Get the end of the period"""

print('\n--- Creating ending period ---')

def get_end_period():
  """
  Asks the users the year, month, and date (INT) and convert it into 
  datetime format. It will handle any misinput from the users.
  Returns a datetime object.
  """

  while True: 
    try:
      end_year = int(input('Please enter the end year: '))
    except ValueError: 
      print('Please do not enter words')
      continue
    if end_year < 0:
      print('You cannot have a negative year...')
      continue
    elif len(str(end_year)) != 4:
      print("Please enter the year in the correct format. For example '2001'")
      continue
    else: 
      break 

  while True: 
    try:
      end_month = int(input('Please enter the end month: '))
    except ValueError: 
      print('Please do not enter words')
      continue
    if end_month < 0:
      print('You cannot have a negative year...')
      continue
    elif len(str(end_month)) > 2:
      print("Please enter the month in the correct format. For example '2' or 12")
      continue
    else: 
      break 

  while True: 
    try:
      end_date = int(input('Please enter the end date: '))
    except ValueError: 
      print('Please do not enter words')
      continue
    if end_date < 0:
      print('You cannot have a negative date...')
      continue
    elif len(str(end_date)) > 2:
      print("Please enter the date in the correct format. For example '2' or 12")
      continue
    else: 
      break 

  end_date = datetime.date(end_year, end_month, end_date)

  return end_date


end_date = get_end_period()

"""## 2.3 Get the price data within the start and end interval"""

def get_price_data(start_date, end_date, securities):
  """
  Accepts start_date, end_date and LIST of securities. 
  Based on that, Returns a pandas dataframe of the historical price data for 
  all the securities in the list from the start to end date. 
  """

  daily_adjclose_df = pd.DataFrame()

  for security in securities:
      daily_adjclose_df[security] = web.DataReader(security, data_source='yahoo', start = start_date, end = end_date)['Adj Close']

  return daily_adjclose_df


daily_adjclose_df = get_price_data(start_date, end_date, securities)

"""# Step 2. Calculate the expected returns of each ticker

## 2.1 Provide the users with preliminary information on the available methods that we could use for calculating expected returns
"""

def expected_returns_intro_text():
  """
  Provides introduction to the different methods available for estimating
  expected returns of each stock. 
  """

  print('\n--- Estimating expected returns ---\n')
  print('This calculator offers three ways to estimate the'\
        ' expected returns of each stock: ')
  print('1. Using the mean of historical returns')
  print('2. Using the exponentially weighted mean (EMA) of historical returns')
  print('3. Using the CAPM method to estimate the expected returns')


expected_returns_intro_text()

def er_method_brief_explanation():
  """
  Provides the option to read a brief explanation about each available method
  for estimating the expected returns. 
  """

  while True:
    er_info = input("\nFor brief explanation of any of the method,"\
                    " type 'Y' for yes, or else, type 'N' for no: ")
    if er_info.upper() not in ('Y', 'N'):
      print("Please input either 'Y' or 'N'")
      continue
    elif er_info.upper() == 'Y':
      while True: 
        print('\nWhich method would you want a brief explanation about? ')
        while True: 
          method = input("Type '1' for the first method, type '2' for"\
                         " the second, and '3' for the third one: ")
          if method not in ('1', '2', '3'):
            print("Please input either '1', '2', or '3'")
            continue
          elif method == '1':
            print('\METHOD 1. The mean historical return method uses the'\
                  ' daily adjusted closing price data within the time'\
                  ' interval specified by you, and calculate the'\
                  ' annualized average return of each stock.')
            break
          elif method == '2':
            print('\METHOD 2. The EMA historical return method uses the'\
                  ' daily adjusted closing price data within the time interval'\
                  ' specified by you, and calculate the'\
                  ' annualized average return of each stock.'\
                  ' HOWEVER, giving more weight to more recent data.')
            break
          elif method == '3':
            print('\METHOD 3. This method uses the CAPM formula to estimates'\
                  ' the expected return of each stock:')
            print('Expected return = risk_free rate + beta of the company *'\
                    '(market risk premium - risk_free rate)')
            break
        while True:
          continue_explain = input("\nDo you want to know more about the"\
                                   " other methods? Input 'Y' for yes or"\
                                   " 'N' for no: ")
          if continue_explain.upper() not in ('Y', 'N'):
            print("Please input either 'Y' or 'N'")
            continue
          else: 
            break
        if continue_explain.upper() == 'N':
          break
        elif continue_explain.upper() == 'Y':
          continue
      break
    elif er_info.upper() == 'N':
      break


er_method_brief_explanation()

"""## 2.2 Choose a method and calculate our expected returns"""

def get_expected_returns(daily_adjclose_df):
  """
  Accepts the pandas dataframe daily_adjclose_df, then asks the users for the 
  method to be used for estimating expected returns. Handlles any misinput
  from the users. Returns a date type object of ticker symbols and their
  expected returns
  """
  mu = 0 

  while True: 
    choice = input("\nTo choose a method to estimate expected returns,"\
                   " input '1' for the first method, '2' for the second,"\
                   " and '3' for the third: ")
    if choice not in ('1', '2', '3'):
      print("Please input either '1', '2', or '3'")
      continue
    elif choice == '1':
      print('Estimating expected returns based on mean historical returns...')
      mu = expected_returns.mean_historical_return(daily_adjclose_df)
      print('DONE')
      break
    elif choice == '2':
      print('Estimating expected returns based on EMA historical returns...\n')
      print('How recent do you want to give more weight to?')
      print('The default value is 500 days. However, the higher the days, '\
            'the more similar this method is to the first method')
      span = int(input("\nPlease input an integer." 
            " For example, '365' means giving more "\
            "weight to the last 365 trading days: "))
      mu = expected_returns.ema_historical_return(daily_adjclose_df)
      print('DONE')
      break
    elif choice == '3':
      print('\nEstimating expected returns based on CAPM...')
      mu = expected_returns.capm_return(daily_adjclose_df)
      print('DONE')
      break
  return mu 

mu = get_expected_returns(daily_adjclose_df)

"""# Step 3. Calculate our risk model (covariance matrix)

## 3.1 Provide the users with preliminary information on the available methods that we could use for calculating the covariance matrix
"""

def risk_model_intro_text():
  """
  Provides introduction to the different methods available for calculating 
  the covariance matrix
  """

    print('\n--- Calculating risk model ---\n')
    print('This calculator offers three ways to estimate the' \
          ' expected returns of each stock: ')
    print('1. Using the sample covariance matrix')
    print('2. Using the exponentially weighted covariance matrix')
    print('3. Using the shrunk covariance matrices, specifically the' \
          ' Ledoit Wolf constant variance shrinkage method')


risk_model_intro_text()


def rm_method_brief_explanation():
  """
  Provides the option to read a brief explanation about each available method
  for calculating the covariance matrix
  """

  while True:
    rm_info = input("\nFor brief explanation of any of the method,"\
                    " type 'Y' for yes, or else, type 'N' for no: ")
    if rm_info.upper() not in ('Y', 'N'):
      print("Please input either 'Y' or 'N'")
      continue
    elif rm_info.upper() == 'Y':
      while True: 
        print('\nWhich method would you want a brief explanation about? ')
        while True: 
          method = input("Type '1' for the first method, type '2'"\
                         " for the second, and '3' for the third one: ")
          if method not in ('1', '2', '3'):
            print("Please input either '1', '2', or '3'\n")
            continue
          elif method == '1':
            print('\nMETHOD 1. This method creates a covariance matrix,'\
                  ' using the daily adjusted closing price data, by simply'\
                  ' calculating the sample covariances between each stock.'\
                  ' For calculating a risk model, this is the most'\
                  ' simple method and therefore is not recommeded.')
            break
          elif method == '2':
            print('\nMETHOD 2. This method creates a covariance matrix,'\
                  ' using the daily adjusted closing price data,' \
                  ' by calculating the sample covariances between each stock,'\
                  ' but also giving more weight to more recent data.')
            break
          elif method == '3':
            print('\nMETHOD 3. A more detailed and technical explanation'\
                  ' of this method can be found here: '\
                  'https://reasonabledeviations.com/notes/papers/ledoit_wolf_covariance/')
            print('\nIn short, this method is superior compared to both'\
                  ' other methods. It is the result of compromising between'\
                  ' an unstrcutred and structured covariance estimator to'\
                  ' create one that has an overall lower'\
                  ' estimation error and bias.')
            break
        while True:
          continue_explain = input("\nDo you want to know more about the other "\
                                   "methods? Input 'Y' for yes or 'N' for no: ")
          if continue_explain.upper() not in ('Y', 'N'):
            print("Please input either 'Y' or 'N'")
            continue
          else:
            break
        if continue_explain.upper() == 'N':
          break
        elif continue_explain.upper() == 'Y':
          continue
      break
    elif rm_info.upper() == 'N':
      break

rm_method_brief_explanation()

"""## 3.2 Choose a method and calculate our risk model (covariance matrix)"""

def get_risk_model(daily_adjclose_df):
  """
  Accepts the pandas dataframe daily_adjclose_df, then asks the users for the 
  method to be used for calculating covariance matrix. Handlles any misinput
  from the users. Returns a data type of the covariance matrix of the securities
  """
  
  covariance_matrix = 0 

  while True: 
    choice = input("\nTo choose a method to calculate our risk model,"\
                   " input '1' for the first method, '2' for the second"\
                   " and '3' for the third: ")
    if choice not in ('1', '2', '3'):
      print("Please input either '1', '2', or '3'")
      continue
    elif choice == '1':
      print('\nCalculating our risk model using the sample covariance matrix...')
      covariance_matrix = risk_models.sample_cov(daily_adjclose_df)
      print('DONE')
      break
    elif choice == '2':
      print('\nCalculating our risk model using the exponentially weighted'\
            'covariance matrix...')
      print('\nHow recent do you want to give more weight to?')
      print('The default value is 180 days. However, the higher the days, '\
            'the more similar this method is to the first method')
      print('The days input here should also be the same as the date input'\
            ' for EMA historical return, if you had chosen that method.')
      span = int(input("\nPlease input an integer." 
            " For example, '365' means giving more "\
            "weight to the last 365 trading days: "))
      covariance_matrix = risk_models.exp_cov(daily_adjclose_df)
      print('DONE')
      break
    elif choice == '3':
      print('\nCalculating our risk model using the'\
            ' Ledoit Wolf constant variance shrinkage method...')
      covariance_matrix = risk_models.risk_matrix(daily_adjclose_df, \
                          method='ledoit_wolf_constant_variance')
      print('DONE')
      break

  # Fix the covariance matrix if it is not positive semidefinite    
  covariance_matrix_fix = risk_models.fix_nonpositive_semidefinite(covariance_matrix)

  return covariance_matrix_fix 


covariance_matrix = get_risk_model(daily_adjclose_df)

"""# Step 4. Optimize our portfolio

## 4.1 Ask whether if there is a weight requirement (min/max) for each stock
"""

def get_weight_bounds(securities): 
  """
  Accepts the LIST of securities. Asks the user whether they want to specify 
  weight bounds for the securities. Returns a list of tuples, or None. 
  """
  
  print("\nBefore getting our asset allocation, do you have"\
      " any requirement about the allocation of each"\
      " stock? For example, you can require minimum"\
      " weight of all stock to be 20% and maximum to be"\
      " 80% of the portfolio, or you can specify a different "\
      " weight requirement for each company.")
  
  min = 0 
  max = 0
  while True:
    weight_requirement = input("Input 'Y' for yes, or 'N for no: ")
    if weight_requirement.upper() not in ('Y', 'N'):
      print("\nPlease input either 'Y' or 'N'")
      continue  
    elif weight_requirement.upper() == 'Y':
      print('\nDo you want to set the min/max weight the same for all stock'\
            ' or for each stock?')
      while True:
        all_or_each = input("Input either 'all' or 'each': ")
        if all_or_each.upper() not in ('ALL', 'EACH'):
          print("'Please only input either 'all' or 'each'")
          continue
        elif all_or_each.upper() == 'ALL':
          while True:
            try:
              min = float(input("Please input the minimum weight."\
                                " For example, '0.2' for 20%: "))
              max = float(input("Please input the maximum weight."\
                                " For example, '0.8' for 80%: "))
            except ValueError:
              print("Please enter the value in the format"\
                    " shown in the examples")
              continue
            if min < 0.0 or max > 1:
              print("The minimum weight cannot be"\
                    " lower than '0' and the maximum weight"\
                    " cannot be larger than '1'")
              continue
            else:
              weight_bounds_all = (min, max)
              break
            break
          break
        elif all_or_each.upper() == 'EACH':
          weight_bounds_each = []
          for security in securities: 
            print(f'\nFor {security}: ')
            while True:
              try: 
                min = float(input("Please input the minimum weight."\
                                  " For example, '0.2' for 20%: "))
                max = float(input("Please input the maximum weight."\
                                  " For example, '0.8' for 80%: "))
              except ValueError:
                print("Please enter the value in the format"\
                      " shown in the examples")
                continue
              if min < 0.0 or max > 1:
                print("The minimum weight cannot be lower than '0'"\
                      " and the maximum weight cannot be larger than '1'")
                continue
              else: 
                weight_bounds_each.append((min, max))
                break 
          break
      break
    elif weight_requirement.upper() == 'N':
      break

  if weight_requirement.upper() == 'Y':
    if all_or_each.upper() == 'ALL':
      return weight_bounds_all
    elif all_or_each.upper() == 'EACH':
      return weight_bounds_each
  elif weight_requirement.upper() == 'N':
    return None

weight_bounds = get_weight_bounds(securities)

"""# 4.2 Generating our efficient frontier object (not relevant to the users)"""

def get_efficient_frontier_object(mu, covariance_matrix, weight_bounds):
  """
  Accepts data type objects mu, covariance_matrix, and list of tuples or None. 
  Returns EfficientFrontier object created by the PyPortfolioOpt library.
  """

  # Set default weight bound if user chooses not to set it themselves
  if weight_bounds == None:
    weight_bounds = (0,1)

  efficient_frontier_object = EfficientFrontier(mu, covariance_matrix, weight_bounds)
  efficient_frontier_object.add_objective(objective_functions.L2_reg, gamma=0.1)

  return efficient_frontier_object


efficient_frontier_object = get_efficient_frontier_object(mu, covariance_matrix, weight_bounds)

"""## 4.3 Provide preliminary information on the available methods that we could use to optimize our portfolio """

def optimizing_method_text():
  """
  Provides introduction to the different methods available for mean-variance 
  optimization of the portfolio.
  """
    print('--- Optimizing your portfolio ---\n')
    print('This calculator offers four different goals to optimize' \
          ' your portfolio: ')
    print('1. Optimizes for maximum Sharpe ratio')
    print('2. Optimizes for minimum portfolio volatility')
    print('3. Optimizes for efficient risk')
    print('4. Optimizes for efficient return')


optimizing_method_text()

def optimizing_method_brief_explanation():
  """
  Provides the option to read a brief explanation about each available method
  for optimizing the portfolio
  """

  while True:
    opt_info = input("\nFor brief explanation of any of the method, type 'Y' "
                    "for yes, or else, type 'N' for no: ")
    if opt_info.upper() not in ('Y', 'N'):
      print("Please input either 'Y' or 'N'")
      continue
    elif opt_info.upper() == 'Y':
      while True: 
        print('\nWhich method would you want a brief explanation about? ')
        while True: 
          method = input("Type '1' for the first method, '2' for the second,"\
                         " '3' for the third, and '4' for the fourth one: ")
          if method not in ('1', '2', '3', '4'):
            print("Please input either '1', '2', '3', or '4'")
            continue
          elif method == '1':
            print('\nMETHOD 1. Sharpe ratio is the excess in return by holding'\
                  ' risky asset for the extra volatility\n')
            print('Sharpe ratio = (portfolio return - risk_free rate) / '\
                  'portfolio volatility\n')
            print('This method generates all possible combination of '\
                  ' asset weight allocation (not including shorts), calculate'\
                  'the portfolio return and volatitlity, and chooses the '\
                  'combination that results in the highest Sharpre ratio')
            break
          elif method == '2':
            print('\nMETHOD 2. This method aims to create a portfolio with'\
                  ' the minimum volatity')
            break
          elif method == '3':
            print('\nMETHOD 3. This method will try to maximize the portfolio'\
                  ' return with a given target volatility')
            break
          elif method == '4':
            print('\nMETHOD 4. This method will try to minimize the portfolio'\
                  ' volatility with a given target return')
            break  
        while True: 
          continue_explain = input("\nDo you want to know more about the other "
                                 "method? Input 'Y' for yes or 'N' for no: ")
          if continue_explain.upper() not in ('Y', 'N'):
            print("Please input either 'Y' or 'N'")
            continue
          else: 
            break
        if continue_explain.upper() == 'N':
          break
        elif continue_explain.upper() == 'Y':
          continue
      break
    elif opt_info.upper() == 'N':
      break


optimizing_method_brief_explanation()

"""## 4.4 Choose our optimizing method and calculate the optimal weight distribution of each stock"""

def optimizes(efficient_frontier_object):
  """
  Accepts the EfficientFrontier object, then asks the users for the 
  method to be used for optimizing the portfolio. Handlles any misinput
  from the users. Returns an OrderedDict of ticker symbols and their weight 
  distribution"
  """

  asset_weight_allocation = 0 

  while True: 
    choice = input("To choose a method to optimize your portfolio, input '1' "
                   "for the first method, '2' for the second, "\
                   "'3' for the third, or '4' for the fourth: ")
    if choice not in ('1', '2', '3', '4'):
      print("Please input either '1', '2', '3', or '4'")
      continue
    elif choice == '1':
      print('Optimizing for maximum Sharpe ratio...')
      asset_weight_allocation = efficient_frontier_object.max_sharpe()
      print('DONE')
      break
    elif choice == '2':
      print('Optimizes for minimum portfolio volatility...')
      asset_weight_allocation = efficient_frontier_object.min_volatility()
      print('DONE')
      break
    elif choice == '3':
      print('Optimizing for efficient risk...')
      while True:
        try: 
          target_volatility = float(input("Please input your desired portfolio volatlity."\
                                          " For example, '0.3' for at most 30% annual volatility: "))
        except ValueError:
          print("Please enter the value in the format shown in the examples")
          continue
        if float(target_volatility) < 0.0 or target_volatility > 1:
          print("The target volatility cannot be lower than 0 or larger than 1")
          continue
        else:
          asset_weight_allocation = efficient_frontier_object.efficient_risk(target_volatility)
          print('DONE')
          break 
      break
    elif choice == '4':
      print('Optimizing for efficient return...')
      while True:
        try: 
          target_return = float(input("Please input your desired portfolio return."\
                                        " For example, '0.3' for at least 30% annual return: "))
        except ValueError:
          print("Please enter the value in the format shown in the examples")
          continue
        if float(target_return) < 0.0 or target_return > 1:
          print("The target volatility cannot be lower than 0 or larger than 1")
          continue
        else:
          asset_weight_allocation = efficient_frontier_object.efficient_return(target_return)
          break 
          print('DONE')
      break

  return asset_weight_allocation


efficient_frontier_object = get_efficient_frontier_object(mu, covariance_matrix, weight_bounds)
asset_weight_allocation = optimizes(efficient_frontier_object)

"""## 4.5 Calculate the optimal discrete allocation of each ticker"""

def get_discrete_allocation (asset_weight_allocation):
  """
  Accepts the OrderedDict of asset_weight_allocation, finds the latest prices of
  each security in the portfolio and calculate the discrete allocation of each 
  ticker. Returns a tuple that includes a dicitonary of (KEYS) ticker symbols
  and (VALUES) of INT, and FLOAT remaining money.
  """

  latest_prices = get_latest_prices(daily_adjclose_df)
  discrete_allocation_object = DiscreteAllocation(asset_weight_allocation, latest_prices, total_portfolio_value)
  greedy_allocation = discrete_allocation_object.greedy_portfolio()

  return greedy_allocation


portfolio_discrete_allocation = get_discrete_allocation (asset_weight_allocation)
print(portfolio_discrete_allocation)

"""# Step 5. Display the results and expected performance of the optimized portfolio"""

def display_weight_allocation(portfolio_discrete_allocation):
  """
  Accepts the OrderedDict discrete portfolio allocaion and prints out the
  information to the users 
  """

  print(f'With ${total_portfolio_value:,.0f} you could buy:')
  for ticker, number_of_stock in portfolio_discrete_allocation[0].items():
    print(f'{number_of_stock} {ticker}')
  print(f'and still have ${portfolio_discrete_allocation[1]:.2f} left')

display_weight_allocation(portfolio_discrete_allocation)

def print_portfolio_performance():
  """
  Calculates the expected annual return and volatility of the portfolio, and 
  its Sharpe ratio, and print out the information to the users
  """

  performance = efficient_frontier_object.portfolio_performance(verbose=False)
  print(f'Expected annual return of this portfolio: {performance[0]*100:.1f}%')
  print(f'Expected annual volatility of this portfolio: {performance[1]*100:.1f}%')
  print(f'Sharpe Ratio: {performance[2]:.2f}')

print_portfolio_performance()