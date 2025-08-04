from .base_models import *
from typing import List

class SchemeUser(BaseUser):
    role: BaseRole

class SchemeAd(BaseAd):
    author: BaseUser
    category: BaseCategory


class SchemeResponse(BaseResponse):
    ad: BaseAd
    category: BaseCategory

class SchemeFavorite(BaseFavorite):
    ad: BaseAd
    user: BaseUser