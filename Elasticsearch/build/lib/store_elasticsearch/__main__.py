#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as  ConnectElasticsearch
import store_elasticsearch.create_index as  CreateIndex 
import store_elasticsearch.store_row as  StoreRow
import store_elasticsearch.store_youtube_driver as StoreYoutubeDriver
import store_elasticsearch.store_discord_driver as StoreDiscordDriver
import store_elasticsearch.store_instagram_driver as StoreInstagramDriver

import click
@click.command()
@click.option('--company_name', default="", help='The company name.')


def main(company_name):

    ''' 
    Store data in Elasticsearch.
    '''

    if (len(str(company_name)) > 0):
        click.echo('Storing discord data')
        storeDiscordDriver = StoreDiscordDriver.StoreDiscordDriver(str(company_name))    # Store discord-driver data.
        storeDiscordDriver.store_discord_driver()

        click.echo('Storing youtube data')
        storeYoutubeDriver = StoreYoutubeDriver.StoreYoutubeDriver(str(company_name))    # Store youtube-driver data.
        storeYoutubeDriver.store_youtube_driver()
		
        click.echo('Storing instagram data')
        storeInstagramDriver = StoreInstagramDriver.StoreInstagramDriver(str(company_name))    # Store instagram-driver data.
        storeInstagramDriver.store_instagram_driver()

    else:
        click.echo('Enter the company name')
		