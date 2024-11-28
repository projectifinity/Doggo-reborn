import requests, json


def drama_link(dramaData):

    if ( bool(dramaData['results']) == False ):
        dramaLink = ('Drama could not be found.')
    else:
        mdlSlug = dramaData['results'][0]['slug']
        dramaLink = ('https://mydramalist.com/' + mdlSlug)

    return dramaLink