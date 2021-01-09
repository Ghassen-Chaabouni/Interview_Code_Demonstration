

import click
import os,sys

import __init__ as initia

@click.command()
@click.option('--name' , default="" , help='enter profil name')
def insta(name):
	p = initia.InstaDriver()
	click.echo(p.get_user_info(name)) 