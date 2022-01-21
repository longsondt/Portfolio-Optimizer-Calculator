## Introduction
- This is a python calculator that I have built that can create an optimized American stock portfolio for the users. 
The primary library used for this prgoram is the *PyPortfolioOpt* library created by 
[Robert Martin](https://github.com/robertmartin8) 

- __All__ the technical/quantitative finance related calculations are performed by the functions using the __PyPortfolioOpt__ library.
Therefore, the goal of this program is to provide a quick and handy optimizer that presents the functions in a user-friendly way, 
so that a *beginner-level* finance enthusiast could use to create an optimized stock portfolio and get a taste of quantitative finance. 

 ## How it works
 - The calculator will ask for the users input for the total amount of fund they want to invest in the portfolio, 
 the number of companies they want to invest in, and the names of those companies. 
 - Then, it will grab the historical price data for those stocks, within the starting and ending period, 
 specified by the users. 
 - Then, the program will use the functions provided by *PyPortfolioOpt* to calculate the *expected returns* of each stock, 
 the *covariance matrix*, and the *weight allocation based on the optimizing goals*, all of which are specified by 
 the users before calculation. 
 - Finally, it will print out the discrete allocaiton of each stock, the money remaining after buying, and the expected performance 
 and the Sharpe Ratio of the optimized portfolio. 
 
  ## Features
1. Suggests discrete allocation of the securities in the portfolio based on the mean-variance analysis. 
2. Provides three different methods to estimating expected returns of each stock (*Mean historical returns, EMA historial returns, and CAPM returns*), 
three different methods to calculate the risk model (*Sample-covariance, exponentially-weighted covariance, and shrinkage covariance matrix*), 
and four different ways to optimize the portfolio (*Optimizes for max Sharpe ratio, optimizes for minimum volatility, optimizes for efficient return, and optimized for efficient risk*) 
3. Automatically grabs historical price data for the users.
4. Allows the users to specify, if they wanted, the weight bound requirement for each, or all tickers in the portfolio. 
5. Handles any invalid input from the user without breaking or requiring the restarting the program 
 
  ## Some limitations of this calculator...
   __1. The calculation methods provided in this calculator are not all the methods that you can use to optimize your portfolio...__
  #### Why?
  - As mentioned before, all the technical/quantitative finance related calculations are performed by the functions *borrowed* from the __PyPortfolioOpt__ library.
    Robert Martin has created an amazing and extensive library for any finance enthusiast or professional expert to use for their portfolio. Meaning, the library offers many 
    different ways to estimate the expected returns, calcualte the covariance matrix, and optimization goals, with varrying complexities that must be accompanied by strong 
    quantitave and financial theory. 
  - Since the goal of the calcualtor is to provide a quick way to create an optimized portfolio for *beginners*, only the more straight-forward/textbok-default methods 
   are included. 
   
   __2. This calculator only works with tickers available on Yahoo Finance__
   #### Why?
   - One of the feature of this calculator is being able to handle any misinput without breaking, which includes handling typo of stock ticker. So far, the only way I have 
   been able to do that is to use a *yfinance* library function to check each time whether the ticker the users have inputted is correct or not. Therefore, tickers that 
   are not on Yahoo! Finance will not work. 
   
  ## How to try the program
  The best way to try the program without needing to have an IDE is to download the Portfolio_Optimization_Calculator.**ipynb** file and run it with [Google Colab](https://research.google.com/colaboratory/).
    
