import run
app =run.create_app()

# Feed_ratio not in but page in
def test_for_long_page_number():
    with app.test_client() as test1:
        res1 = test1.get("http://localhost:5000/api/properties?page=22")
        assert res1.status_code == 400

def test_for_valid_page_number():
    with app.test_client() as test2:
        res2 = test2.get("http://localhost:5000/api/properties?page=2")
        assert  res2.status_code == 200

def test_for_invalid_page_number():
    with app.test_client() as test3:
        res3 = test3.get("http://localhost:5000/api/properties?page=abcdefgh")
        assert  res3.status_code ==400

# Feed_ratio and page number not in url

def test_for_properties_validation():
    with app.test_client() as test4:
        res4 = test4.get("http://localhost:5000/api/properties")
        assert res4.status_code == 200
# Feed_ratio and page number in url
def test_for_valid_feed_ratio():
    with app.test_client() as test5:
        res5 = test5.get("http://localhost:5000/api/properties?feed_ratio=[{%27feed%27:11,%27ratio%27:15},{%27feed%27:12,%27ratio%27:25},{%27feed%27:16,%27ratio%27:8}]&page=1")
        assert res5.status_code == 200

def test_for_invalid_feed_ratio():
    with app.test_client() as test6:
        res6 = test6.get("http://localhost:5000/api/properties?feed_ratio=[{'feed':11,'ratio':25},{'feed':12,'ratio':25},{'feed':16,'ratio':25}]&page=1")
        assert res6.status_code == 400
def test_for_invalid_feed_ratio_type_error():
    with app.test_client() as test7:
        res7 = test7.get("http://localhost:5000/api/properties?feed_ratio=[{%27feed%27:11,%27ratio%27:25},{%27feed%27:12,%27ratio%27:25},{%27feed%27:16,%27ratio%27:25}]&page=axyz")
        assert res7.status_code == 400
def test_success_feed_ratio_type_error():
    with app.test_client() as test8:
        res8 = test8.get("http://localhost:5000/api/properties?feed_ratio=[{%27feed%27:11,%27ratio%27:16},{%27feed%27:12,%27ratio%27:16},{%27feed%27:16,%27ratio%27:16}]&page=1")
        assert res8.status_code == 200