from .hist import Data, Check, Process, Env, Session

__version__ = "0.1.0"

data_intervals = Data.intervals
check_symbols = Check.symbols
check_date = Check.date
check_intraday = Check.intraday
process_date = Process.date
# process_url = Process.url
with_env = Env.with_
get_session = Session.get
get_data = Data.get

__all__ = [
    "Data", "data_intervals",
    "Check", "check_symbols", "check_date", "check_intraday",
    "Process", "process_date", # "process_url"
    "Env", "with_env",
    "Session", "get_session",
    "get_data"
]
