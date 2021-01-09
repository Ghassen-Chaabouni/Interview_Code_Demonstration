from .User import User
from .Post import Post
from .Image import Image
import json
import os

from abc import ABC
class Driver(ABC):

    def get_event(self, user_id):
        pass

    def get_page(self, user_id):
        pass
		
    def get_group(self, user_id):
        pass
		
    def get_images(self, user_id):
        pass
		
    def get_user_info_by_pseudo(self, pseudo, json_parser=False):
        pass

    def get_friends(self, user_id):
        pass
		
    def get_react(self, publication_id):
        pass
    
    def get_comment_by_key(self, starttime='', comments='', key=[], json_parser=False, **kwargs):
        pass
    
    def get_comment_by_keys(self, starttime='', comments='', keys=[], json_parser=False, **kwargs):
        pass
		
		
		
    def get_user_info(self, user, **kwargs):
        pass
    
    def get_publications(self, user , starttime, comments, json_parser=False, **kwargs):
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
		
    def get_event(self, user_id):
        pass

    def get_page(self, user_id):
        pass
		
    def get_group(self, user_id):
        pass
		
    def get_friends(self, user_id):
        pass
        
    def save_json(self, data, fname):
        # Append JSON object to output file JSON array
        if os.path.isfile(fname):
            # File exists
            with open(fname, 'a+') as outfile:
                # Move the pointer (similar to a cursor in a text editor) to the end of the file
                outfile.seek(0, os.SEEK_END)

                # This code means the following code skips the very last character in the file -
                # i.e. in the case the last line is null we delete the last line
                # and the penultimate one
                pos = outfile.tell() - 1

                # Read each character in the file one at a time from the penultimate
                # character going backwards, searching for a newline character
                # If we find a new line, exit the search
                while pos > 0 and outfile.read(1) != "\n":
                    pos -= 1
                    outfile.seek(pos, os.SEEK_SET)

                # So long as we're not at the start of the file, delete all the characters ahead
                # of this position
                if pos > 0:
                    outfile.seek(pos, os.SEEK_SET)
                    outfile.truncate()
                outfile.write(',')
                json.dump(data, outfile, indent=2)
                outfile.write('\n')
                outfile.write(']')
        else: 
            # Create file
            with open(fname, 'w') as outfile:
                array = []
                array.append(data)
                json.dump(array, outfile, indent=2)
		
        
    def get_images(self, user='', starttime='', keys=[], download_img=False, json_parser=False, **kwargs):
        p = Image()
        if(not download_img):
            if (not json_parser):
                return p.get_images(user=user, starttime=starttime, keys=keys, **kwargs)
            else:
                data = p.get_images(user=user, starttime=starttime, keys=keys, **kwargs)
                self.save_json(data, "instagram_images.json")                          

        else:
            p.get_images(user=user, starttime=starttime, keys=keys, download_img=download_img, **kwargs)
            
		
    def get_comment_by_key(self, starttime='', comments='', key=[], json_parser=False, **kwargs):
        p = Post()
        if (not json_parser):
            return p.get_posts(starttime=starttime, comments=comments, keys=[key], **kwargs)
        else:
            data = p.get_posts(starttime=starttime, comments=comments, keys=[key], **kwargs)
            self.save_json(data, "instagram_data.json")          
			
    def get_comment_by_keys(self, starttime='', comments='', keys=[], json_parser=False, **kwargs):
        p = Post()
		
        if (not json_parser):
            return p.get_posts(starttime=starttime, comments=comments, keys=keys, **kwargs)
        else:
            data = p.get_posts(starttime=starttime, comments=comments, keys=keys, **kwargs)
            self.save_json(data, "instagram_data.json") 
            
		
    def get_user_info(self,user,**kwargs):
        p = User()
        return p.get_info(user,**kwargs)
    
    def get_publications(self, user , starttime, comments, json_parser=False, **kwargs):
        p = Post()

        if (not json_parser):
            return p.get_posts(user , starttime, comments , **kwargs)
        else:
            data = p.get_posts(user , starttime, comments , **kwargs)
            self.save_json(data, "instagram_data.json") 
            

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
    
   