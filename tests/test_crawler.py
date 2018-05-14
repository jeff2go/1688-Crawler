import pytest


@pytest.mark.fast
def test_crawl_categories(client):
    url = 'https://ywlingpan.1688.com/page/offerlist.htm'
    rv = client.get('/crawlers/categories', query_string=dict(url=url))
    json_data = rv.get_json()
    assert len(json_data['data']) > 0
    assert 'ywlingpan' == json_data['shop']['id']


@pytest.mark.fast
def test_crawl_categories_with_exception(client):
    url = 'https://ywlingpan.1688.com/page/offerlis'
    rv = client.get('/crawlers/categories', query_string=dict(url=url))
    assert rv.status_code == 500
    assert 'errcode' in rv.get_json()


@pytest.mark.fast
def test_crawl_products(client):
    url = 'https://ywlingpan.1688.com/page/offerlist.htm?pageNum=1'
    rv = client.get('/crawlers/products', query_string=dict(url=url))
    json_data = rv.get_json()
    assert len(json_data['data']) > 0
    assert 'ywlingpan' == json_data['shop']['id']


@pytest.mark.fast
def test_crawl_products_with_exception(client):
    url = 'https://ywlingpan.1688.com/page/offerlist'
    rv = client.get('/crawlers/products', query_string=dict(url=url))
    assert rv.status_code == 500
    assert 'errcode' in rv.get_json()


@pytest.mark.product
def test_crawl_product(client):
    url = 'https://detail.1688.com/offer/1152061078.html'
    rv = client.get('/crawlers/product', query_string=dict(url=url))
    json_data = rv.get_json()
    assert 'title' in json_data
    assert '1152061078' == json_data['offerid']


@pytest.mark.fast
def test_crawl_product_with_exception(client):
    url = 'https://detail.1688.com/offer/1152061078'
    rv = client.get('/crawlers/product', query_string=dict(url=url))
    assert rv.status_code == 500
    assert 'errcode' in rv.get_json()


@pytest.mark.slow
def test_crawl_product_100_times(client):
    url = 'https://detail.1688.com/offer/1152061078.html'
    for i in range(1, 101):
        rv = client.get('/crawlers/product', query_string=dict(url=url))
        json_data = rv.get_json()
        assert 'title' in json_data
        assert '1152061078' == json_data['offerid']
