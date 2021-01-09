from .User import User
from .Post import Post


from abc import ABC
class Driver(ABC):

    def get_user_info(self, user, **kwargs):
        pass
    
    def get_publications(self, user , starttime, comments , **kwargs):
        pass

    def get_comment_by_publication(self, publication_id , **kwargs):
        pass
    
    def get_posts_from_keys(self, list_key , **kwargs):
        pass

    def get_profile_pic(self , user , **kwargs):
        pass

    def get_last_pic(self, user , **kwargs):
        pass

    def get_last_location(self,user):
        pass

    def get_number_publications(self,user):
        pass
    
    def get_number_followers(self,user):
        pass

    def get_number_followed(self,user):
        pass

    def get_last_post_date(self,user):
        pass

    def get_last_post_likes(self,user):
        pass

class InstaDriver(Driver):
    def __init__(self):
        pass

    def get_user_info(self,user,**kwargs):
        p = User()
        return p.get_info(user,**kwargs)
    
    def get_publications(self, user , starttime, comments , **kwargs):
        p = Post()
        return p.get_posts(user , starttime, comments , **kwargs)

    def get_comment_by_publication(self, publication_id , **kwargs):
        p = Post()
        return p.get_comment_by_publication(publication_id , **kwargs)

    def get_profile_pic(self, user , **kwargs):
        p = User()
        return p.get_profile_pic(user,**kwargs)

    def get_last_pic(self, user , **kwargs):
        p = User()
        return p.get_last_image(user,**kwargs)

    def get_number_publications(self, user):
        p = User()
        return p.get_number_publications(user)

    def get_number_followers(self, user):
        p = User()
        return p.get_number_followers(user)

    def get_number_followed(self, user):
        p = User()
        return p.get_number_followed(user)
    
    def get_last_post_date(self, user):
        p = User()
        return p.get_last_post_date(user)
    
    def get_last_post_likes(self, user):
        p = User()
        return p.get_last_post_likes(user)
    
   