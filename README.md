# 1688-Crawler

Based on Flask, require python3.9

## Install

Create a virtual environment by venv

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements by pip:

```sh
pip install -r requirements.txt
```

### Config
```shell
mv .env.example .env
```

## Run

```shell
python run.py
```

Open http://127.0.0.1:8080 in a browser.

## API Endpoints

### 1. Get Categories
```
GET /crawlers/categories
```
Retrieves all categories from a 1688 shop home page.
- Query Parameter: `url` - The URL of the 1688 shop home page

### 2. Get Product List
```
GET /crawlers/products
```
Retrieves a list of products from a 1688 shop category or search page.
- Query Parameter: `url` - The URL of a shop product list page

### 3. Get Product Details
```
GET /crawlers/product
```
Retrieves detailed information about a specific product.
- Query Parameter: `url` - The URL of the product detail page
