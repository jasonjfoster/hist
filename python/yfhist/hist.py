import os
import time
import requests
import pandas as pd
import importlib.resources as pkg_resources
import contextlib

class ClassProperty:
  
  def __init__(self, getter):
    self.getter = getter
  
  def __get__(self, instance, owner):
    return self.getter(owner)
  
class Data:

  _intervals = None
  
  @ClassProperty
  def intervals(cls):
    """
    Intervals Data for the Yahoo Finance API
    
    A data frame with the available intervals data for the Yahoo Finance API.
    
    Returns:
      A data frame.
    """

    if cls._intervals is None:
      data_path = pkg_resources.files("yfhist") / "data" / "intervals.csv"
      cls._intervals = pd.read_csv(data_path)

    return cls._intervals

class Check:
  
  @staticmethod
  def symbols(symbols):
  
    if isinstance(symbols, str):
      symbols = [symbols]
    
    valid_symbols = (isinstance(symbols, (list, tuple)) and len(symbols) > 0 and
      all(isinstance(s, str) and s.strip() != "" for s in symbols))
      
    if not valid_symbols:
      raise ValueError("invalid 'symbols'")
  
  @staticmethod
  def date(date, type):
  
    try:
      pd.to_datetime(date, format = "%Y-%m-%d")
    except ValueError:
      raise ValueError(f"invalid '{type}'")
    
  @staticmethod
  def interval(interval):
  
    valid_interval = set(Data.intervals["field"])
    
    if interval not in valid_interval:
      raise ValueError("invalid 'interval'")
    
  @staticmethod
  def intraday(from_date, to_date, interval):
    
    from_date = pd.to_datetime(from_date, utc = True).normalize()
    to_date = pd.to_datetime(to_date, utc = True).normalize()
    
    valid_lookback = Data.intervals.loc[Data.intervals["field"] == interval, "lookback"].iloc[0]
    
    if (to_date - from_date).days <= 0:
      raise ValueError("value of 'to_date' must be greater than 'from_date'")
    
    if (interval == "1m") and ((to_date - from_date).days > 8):
      raise ValueError("number of days between 'from_date' and 'to_date' must be less than or equal to 8")
    
    today_utc = pd.Timestamp.now(tz = "UTC").normalize()
    if ~pd.isna(valid_lookback) and ((today_utc - from_date).days >= valid_lookback):
      raise ValueError(f"number of days between 'from_date' and today must be less than {valid_lookback}")

class Process:
  
  @staticmethod
  def date(date):
  
    result = int(pd.to_datetime(date, utc = True).timestamp()) # 64-bit
    
    return result
  
  # @staticmethod
  # def url(params):
  #   
  #   result = "?" + "&".join(f"{key}={value}" for key, value in params.items())
  #   
  #   return result
  
class Env:
  
  @staticmethod
  @contextlib.contextmanager
  def with_(new_env):
    
    old_env = {}
  
    try:
  
      for name, value in new_env.items():
  
        old_env[name] = os.environ.get(name)
  
        if value is None:
          os.environ.pop(name, None)
        else:
          os.environ[name] = value
  
      yield
  
    finally:
      
      for name, value in old_env.items():
        
        if value is None:
          os.environ.pop(name, None)
        else:
          os.environ[name] = value

class Session:
  
  @staticmethod
  def get():
    """
    Get the Crumb, Cookies, and Handle for Yahoo Finance API
    
    A method to get the crumb, cookies, and handle required to authenticate and interact
    with the Yahoo Finance API.
    
    Returns:
      A dictionary containing the following elements:
        - "handle" (requests.Session): a session handle object for subsequent requests.
        - "crumb" (str): a string representing the crumb value for authentication.
        - "cookies" (dict): a data frame of cookies for the request.
        
      Examples:
        session = screen.get_session()
    """
    
    session = requests.Session()
    
    api_url = "https://query1.finance.yahoo.com/v1/test/getcrumb"
    
    headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }
    
    session.headers.update(headers)
  
    with Env.with_({"CURL_SSL_BACKEND": "openssl"}):
      response = session.get(api_url)
    
    crumb = response.text.strip()
    cookies = session.cookies.get_dict()
  
    result = {
      "handle": session,
      "crumb": crumb,
      "cookies": cookies
    }
    
    return result
  
def get(symbols, from_date = "2007-01-01", to_date = None, interval = "1d"):
  """
  Get Data from the Yahoo Finance API

  A method to get data from the Yahoo Finance API for symbols using a date
  range and interval.

  Parameters:
    symbols (str or list of str): symbol or list of symbols.
    from_date (str): start date in "YYYY-MM-DD" format (e.g., "2007-01-01").
    to_date (str): end date in "YYYY-MM-DD" format.
    interval (str): data interval (see ``data_intervals``).

  Returns:
    A data frame or dict of data frames that contains data from the
    Yahoo Finance API for the specified symbol(s).
    
  Examples:
    data = yfh.get_data(["AAPL", "MSFT"])
  """
  
  if isinstance(symbols, str):
    symbols = [symbols]

  if to_date is None:
    to_date = pd.Timestamp.now(tz = "UTC")
    
  Check.symbols(symbols)
  Check.date(from_date, "from_date")
  Check.date(to_date, "to_date")
  Check.interval(interval)
  Check.intraday(from_date, to_date, interval)
  
  session = Session.get()
  cookies = session["cookies"]
  handle = session["handle"]
  
  intraday = Data.intervals.loc[Data.intervals["field"] == interval, "intraday"].iloc[0]
  
  if not intraday:
    
    # inclusive end: use midnight after to_date (exclusive bound)
    to_dt = pd.to_datetime(to_date, utc = True).normalize() + pd.Timedelta(days = 1)
    period2 = int(to_dt.timestamp())
    
  else:
    
    # intraday: use exact timestamp
    period2 = Process.date(to_date)
        
  params = {
    "period1": Process.date(from_date),
    "period2": period2,
    "interval": interval
  }
  
  headers = {
    "Content-Type": "application/json",
  }
  
  for key, value in cookies.items():
    handle.cookies.set(key, value)
  
  count = 0
  # result_ls = []
  result_ls = {}
  
  if not intraday:
    cols = ["index", "open", "high", "low", "close", "adjclose", "volume"]
  else:
    cols = ["index", "open", "high", "low", "close", "volume"]

  for symbol in symbols:
    
    api_url = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol # + Process.url(params)
      
    try:
      
      response = handle.get(api_url, params = params, headers = headers)
            
      result = response.json()
      result_df = result["chart"]["result"][0]

    except:
      result_df = pd.DataFrame()

    if (len(result_df) > 0):
      
      tz = result_df["meta"]["exchangeTimezoneName"]
      ohlcv = result_df["indicators"]["quote"][0]
      
      index = result_df["timestamp"]
      
      if not intraday:
        
        adjclose = result_df["indicators"]["adjclose"][0]["adjclose"]
        index = pd.to_datetime(index, unit = "s", utc = True).tz_convert(tz).date
        
        result_df = pd.DataFrame({
          "index": index,
          **ohlcv,
          "adjclose": adjclose
        })
      
      else:
        
        index = pd.to_datetime(index, unit = "s", utc = True).tz_convert(tz)
        
        result_df = pd.DataFrame({
          "index": index,
          **ohlcv
        })
      
      result_df = result_df[cols]
      # result_ls.append(result_df)
      result_ls[symbol] = result_df

    count += 1

    if count % 5 == 0:

      print("pause one second after five requests")
      time.sleep(1)

  if (len(result_ls) == 0):
    return pd.DataFrame()
  elif (len(result_ls) == 1):
    return result_ls[symbols[0]]
  else:
    return result_ls

class Col:
  
  @staticmethod
  def get(data, col):
    """
    Get a Column from the Yahoo Finance API
  
    A method to get a column from the Yahoo Finance API for symbols using a date
    range and interval.
  
    Parameters:
      data (data frame or dict of data frames): data that contains an \code{index} column
      and the requested column created using the \code{\link{get_data}} method.
      col (str): column name to get (i.e., "open", "high", "low", "close", "adjclose", "volume").
  
    Returns:
      A data frame with rows as the \code{index} and columns as the symbols.
      
    Examples:
      data = yfh.get_data(["AAPL", "MSFT"])
      adj = yfh.get_col(data, "adjclose")
    """
    
    if isinstance(data, pd.DataFrame):
      
      result = data.loc[:, ["index", col]].copy()
      result["index"] = pd.to_datetime(result["index"])
      
      # result = result.set_index("index")[[col]]
      
    elif (isinstance(data, dict)):
      
      series_ls = []
    
      for symbol, df in data.items():
    
        df = df.loc[:, ["index", col]].copy()
        df["index"] = pd.to_datetime(df["index"])
    
        df = df.set_index("index")[col]
        df.name = symbol
    
        series_ls.append(df)
    
      result = pd.concat(series_ls, axis = 1)
  
    return result

Data.get = get
