# Seller Analytics

A private analytics platform for Amazon Seller Central.

## Objectives

- Retrieve Amazon orders using the Selling Partner API (SP-API)
- Retrieve Amazon financial transactions
- Maintain a product master and pricing history
- Calculate true order profitability
- Push processed data to Google Sheets
- Build dashboards for business decision making

## Project Structure

```
amazon/        Amazon SP-API integration
google/        Google Sheets integration
models/        Data models
transform/     Business logic and transformations
config/        Configuration
docs/          Documentation
tests/         Unit tests
```

## Roadmap

### Sprint 0
- [x] Development environment
- [x] GitHub
- [x] Virtual Environment

### Sprint 1
- [ ] Amazon Authentication
- [ ] Google Authentication

### Sprint 2
- [ ] Orders Sync

### Sprint 3
- [ ] Financial Events Sync

### Sprint 4
- [ ] Profitability Engine

### Sprint 5
- [ ] Dashboard

### Sprint 6
- [ ] Automation

Current Status

✅ SP-API Authentication
✅ Orders Extraction
✅ Order Items Extraction
✅ Financial Events Extraction
✅ Silver Order Item Transformation
✅ Silver Financial Ledger Transformation
⬜ Gold Profitability Engine
⬜ CSV Export
⬜ Google Sheets Sync
⬜ Daily Automation