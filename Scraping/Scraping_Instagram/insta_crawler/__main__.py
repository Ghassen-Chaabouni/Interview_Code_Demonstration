from .User import User
from .Post import Post
from .Image import Image
import click
import os

os.chdir('crawler')

@click.command()
@click.option('--name', default="", help='enter profil to scrape')
@click.option('--post', default="", help='scraping posts')
@click.option('--start_date', default="", help='The starting date of the posts to scrape.')
def main(name,post,start_date):

    ''' 
        scraping general information from profils in instagram
        using a limit date for posts to scrape  
    '''
    
	if (len(name) > 0) and (len(post) == 0) and (len(start_date) == 0):
        p = User()
        click.echo(p.get_info(name))
    elif (len(name) > 0) and (len(post) > 0) and (len(start_date) == 0):
        p = Post()
        click.echo(p.get_posts(name))
    elif (len(name) > 0) and (len(post) > 0) and (len(start_date)> 0):
        p = Post()
        click.echo(p.get_posts(name,start_date))



if __name__=='__main__':
    main()