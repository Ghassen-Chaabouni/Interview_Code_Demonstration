
from .crawler.crawler.spiders.info import launch
from .crawler.media.media import Media
from .crawler.media.profil import Profil




class User():
    def __init__(self):
        pass
        
                
    def get_info(self, user, **kwargs):
        p = Profil(user)
        return p.get_info()

    def get_profile_pic(self, user, **kwargs):
        m = Media(user)
        return m.get_profile_image(**kwargs)

    def get_last_image(self, user, **kwargs):
        m = Media(user)
        return m.get_last_image(**kwargs)

    def get_last_location(self, user):
        m = Media(user)
        return m.get_last_location()

    def get_number_publications(self, user):
        m = Media(user)
        return m.get_number_publications()

    def get_number_followers(self, user):
        m = Media(user)
        return m.get_number_followers()

    def get_number_followed(self, user):
        m = Media(user)
        return m.get_number_followed()

    def get_last_post_date(self, user):
        m = Media(user)
        return m.get_last_post_date()

    def get_last_post_likes(self, user):
        m = Media(user)
        return m.get_last_post_likes()


