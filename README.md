# CoinBucksAPI
This API is able to Build a simple crypto-to-naira transaction API. ● Accept inputs: amount_in_crypto using the TransactionRequest(BaseModel): class, crypto_type using the EXCHANGE_RATES dictionary, recipient_bank. ● Convert to Naira using a dummy exchange rate. Using the EXCHANGE_RATES dictionary  ● Return transaction details (transaction ID, conversion rate, final amount in Naira) using the TransactionResponse(BaseModel). 
Now for the bonus  ● Add error handling for failed transactions. and ● Implement basic logging (store request & response). I used HTTPException to catch errors and I used the logging library to implement logs
Now If this API was serving thousands of users daily, the improvements and optimizations I added were 

i)Caching • get_exchange_rate is decorated with @cache(expire=300) (cached for 5 minutes).
• Uses in-memory backend by default; easy to switch to Redis in startup().

ii)DB Storage • SQLModel model Transaction stores transactions to the DB in save_transaction_to_db.
• Default DB = sqlite:///./coinbucks.db (local demo).
• To use Postgres, set env var e.g.
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/coinbucks"
and restart — Alembic can be added for migrations as discussed earlier.

iii)Rate Limiting • slowapi Limiter applied; the endpoint has @limiter.limit("20/minute").
• You can tune limits per-route or globally. iv)Async Processing
• Background tasks: FastAPI BackgroundTasks used to persist transaction and run heavy_post_processing non-blocking.
• For real production offload, comment shows how to integrate Celery + Redis (task example).
v)Monitoring
• Prometheus metrics created (REQUEST_COUNTER, TRANSACTION_COUNTER) and exposed at /metrics.
• Configure Prometheus to scrape http://your-host:8000/metrics and build dashboards in Grafana.

This api can be tested via the url https://coinbucksapi.onrender.com 

Now to highlight the mission of this project 
Building this API aligns directly with CoinBucks’ mission of simplifying crypto transactions by turning complex blockchain operations into a clean, user-friendly service. With just a few inputs, users can convert their cryptocurrency into Naira and seamlessly send funds to their local bank, eliminating technical barriers and making crypto accessible to everyday people in Africa.

Now to highlight the vision of this project

As CoinBucks aspires to be Africa’s most trusted crypto payment gateway, this API showcases reliability, transparency, and scalability. By designing it with error handling, logging, and scalability considerations, the service is well-prepared to handle growth and build user confidence. This foundation reflects CoinBucks’ vision of offering secure, fast, and dependable crypto-to-fiat solutions at scale.
