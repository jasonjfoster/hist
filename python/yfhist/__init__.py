from .hist import Data, Check, Process, Env, Session, Col

__version__ = "0.1.0"

data_intervals = Data.intervals
check_symbols = Check.symbols
check_date = Check.date
check_intraday = Check.intraday
check_adjclose = Check.adjclose
process_date = Process.date
# process_url = Process.url
with_env = Env.with_
get_session = Session.get
get_data = Data.get
get_col = Col.get

__all__ = [
    "Data", "data_intervals",
    "Check", "check_symbols", "check_date", "check_intraday", "check_adjclose",
    "Process", "process_date", # "process_url"
    "Env", "with_env",
    "Session", "get_session",
    "get_data",
    "Col", "get_col"
]
