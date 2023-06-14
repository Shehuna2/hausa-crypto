from .models import Post
# from django.core.cache import cache
# from django.views.decorators.cache import cache_page
# import requests

def increase_post_views(post_id):
    post = Post.objects.get(id=post_id)
    post.views += 1
    post.save()

# @cache_page(60 * 5)
# def get_btc_price():
#     btc_price = cache.get("btc_price")
#     if not btc_price:
#         url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=ngn"
#         response = requests.get(url)
#         data = response.json()
#         btc_price = data['bitcoin']['usd']
#         cache.set('btc_price', btc_price)
#     return btc_price
