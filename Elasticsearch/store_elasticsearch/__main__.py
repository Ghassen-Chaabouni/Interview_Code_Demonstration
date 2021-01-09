#!/usr/bin/env python
# coding: utf-8

import store_elasticsearch.connect_elasticsearch as ConnectElasticsearch
import store_elasticsearch.create_index as CreateIndex 
import store_elasticsearch.store_row as StoreRow
import store_elasticsearch.store_profile as StoreProfile
import store_elasticsearch.store_comment as StoreComment
import store_elasticsearch.create_tables as CreateTables

import click
@click.command()
@click.option('--job_name', default="", help='The job name.')
@click.option('--data_type', default="", help='profile or comment')
@click.option('--driver_name', default="", help='driver name: youtube or instagram or discord')



def main(job_name):

    ''' 
    Store data in Elasticsearch.
    '''

    if ((len(str(job_name)) > 0) and (len(data_type) > 0) and (len(driver_name) > 0)):
        if(str(data_type) == "profile"):
            click.echo('Storing profiles')
            storeProfile = StoreProfile.StoreProfile(str(job_name), str(driver_name))    # Store discord-driver data.
            storeProfile.store_profile()
			
        elif(str(data_type) == "comment"):
            click.echo('Storing comments')
            storeComment = StoreComment.StoreComment(str(job_name), str(driver_name))    # Store discord-driver data.
            storeComment.store_comment()
        
    else:
        click.echo('Enter the parameters')
		