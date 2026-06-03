\name{yfhist-package}
\alias{yfhist-package}
\alias{yfhist}
\docType{package}
\title{
  \packageTitle{yfhist}
}
\description{
  \packageDescription{yfhist}
}
\details{

  \code{yfhist} is a package that provides simple and efficient access to Yahoo Finance's history functionality for querying and retrieving financial data.

  The core functionality of the \code{yfhist} package abstracts the complexities of interacting with Yahoo Finance APIs, such as session management, crumb and cookie handling, query construction, date validation, and interval management. This abstraction allows users to focus on retrieving data rather than managing API details. Use cases include retrieving historical data across a range of security types:

  \itemize{
    \item \strong{Equities and ETFs}: end-of-day or intraday Open, High, Low, Close, Volume (OHLCV), and adjusted close prices
    \item \strong{Indices}: levels over time for benchmarking and research
    \item \strong{Other tickers}: additional symbols supported by Yahoo Finance where chart data is available
  }

  The implementation leverages standard HTTP libraries to handle API interactions efficiently and provides support for both R and Python to ensure accessibility for a broad audience.
}
\author{
  \packageAuthor{yfhist}
}
