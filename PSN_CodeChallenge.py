#!/usr/bin/env python3
import pandas as pd
import sys
import datetime as dt
import PSN_tests
import re
import random
import string
from datetime import date

class UserContent:
  def __init__(s,usrs_filename='users',csv_filename='content',user_id=0,request_language='en',oldest_item=None,latest_item=None):
    '''
    :param user_id:          ID of the user making the request. String combination of letters and numbers once set this should not change.
    :param request_language: App language at time of reset. This is a string from preset options.
    :param oldest_item:      item_id (integer) of the item of content currently at
                             the bottom of the feed if requesting older content. None if requesting newer content.
    :param latest_item:      item_id (integer) of the latet item seen by the user
                             (item currently at the top of the feed) if requesting newer content.
                             None if requesting older content.'''

    s.filename=csv_filename+'.csv'
    s.users_filename=usrs_filename+'.csv'
    if user_id==0:
      users=pd.read_csv(s.users_filename)
      s.usr_id=users.loc[1][1]
    else:
      s.usr_id=user_id
    s.oldest_item=oldest_item
    # If the latest_item is None then set the lastest_item id to be the last id in the content
    if latest_item is None:
      content=s.__get_content_csv__()
      s.latest_item=content.index[-1]
    else:
      s.latest_item=latest_item
    s.language=request_language
  def __get_content_csv__(s):
    content=pd.read_csv(s.filename,index_col=1)
    today=pd.Timestamp.today()
    cimpossible=[c for c in content.index if pd.to_datetime(content.loc[c]['created'],format="%Y-%m-%d %H:%M:%S.%f")>today]
    content=content.drop(cimpossible)
    ct0=pd.to_datetime(content.loc[content.index[0]]['created'],format="%Y-%m-%d %H:%M:%S.%f")
    return content
  def __get_user_item__(s):
    users=pd.read_csv(s.users_filename,index_col=1)
    if not s.usr_id in users.index:
      raise KeyError('user_id is not in the dataframe of users')
    return users.loc[s.usr_id]
  def __getitem_with_row__(s,i):
    '''get the itemfor the 'ith' content term'''
    content=s.__get_content_csv__() # Returns a comma separated data frame from the CSV file.
    return content.iloc[i]
  def __getitem_with_id__(s,item_id):
    ''' Return content row using item_id'''
    content=s.__get_content_csv__() # Returns a comma separated data frame from the CSV file.
    return content.loc[item_id]
  def __get_usr_id__(s): return s.usr_id
  def __get_language__(s): return s.language
  def __get_oldest_item__(s): return s.oldest_item
  def __get_latest_item__(s): return s.latest_item
  def __get_filename__(s): return s.filename
  def __set_latest_item__(s,latest_item):
    s.latest_item=latest_item
    s.oldest_item=None
    return
  def __set_oldest_item__(s,oldest_item):
    s.oldest_item=oldest_item
    s.latest_item=None
    return
  def __set_language__(s,language): s.language=language
  def __str__(s):
     content=s.__get_content_csv__()
     return str(content)
  def _usr_row__(s):
    users=pd.read_csv(s.users_filename)
    row=users.get_loc(s.usr_id)
    return row
  def __content_time__(s,item_id):
    ''' Using item_id find the content term and return the timestamp for the term'''
    content=s.__get_content_csv__()
    item=content.loc[item_id]
    datetime_str=item[4]
    datetime_obj=pd.to_datetime(datetime_str,format="%Y-%m-%d %H:%M:%S.%f")
    return datetime_obj
  def row_num_from_id(s,item_id):
    content=s.__get_content_csv__()
    row=content.loc[item_id][0]
    return row
  def id_from_row_num(s,r):
    item=s.__getitem_with_row__(r)
    item_id=item[1]
    return item_id
  def pivot_terms(s):
    ''' Determine whether the content requests are new or old and find the corresponding times.
    The index for the latest_time and oldest_time are checked, if both are not None then an error is raised.
    Else the non-None term determines the direction and the position in content gives the pivot location for searching.
    If both terms are None then no direction is given so return all suitable content.
    The time corresponding to the end of the search and pivot term determine the last_time and first_time.
    assbool is a boolean which gives the direction to sort content, False for descending (newest-oldest)
    and True for ascending (oldest-newest). If latest_time is not None then assbool should be False and if
    oldest_time is not None then assbool should be True.

    :rtype: string, timestamp, timestamp, bool
    :returns: piv1,last_time, first_time, assbool
    '''
    content=s.__get_content_csv__()
    if not s.latest_item is None and not s.oldest_item is None:
      errmsg='both latest_item '+str(s.latest_item)+' and oldest_item '+str(s.oldest_item)
      errmsg+='are not None which should not occur as users either want new or old content.'
      raise TypeError(errmsg)
    elif s.latest_item is None and s.oldest_item is None:
      # since there is no lastest_item or oldest_item all approved content should be returned
      return str(),None,None,False
    elif s.latest_item is None and not s.oldest_item is None:
      last_time=s.__content_time__(content.index[-1])
      first_time=s.__content_time__(s.oldest_item)
      assbool=False
      piv1=s.oldest_item
      return piv1,last_time,first_time,assbool
    elif s.oldest_item is None and not s.latest_item is None:
      today=pd.Timestamp.today()
      last_time=s.__content_time__(s.latest_item)
      first_time=today
      if abs((today-last_time).days)>1:
        # If the latest content is more than a day old then set now to be the start time and view the n_items getting older.
        assbool=False
        piv1=content.index[0]
      else:
        assbool=True
        piv1=s.latest_item
      return piv1,last_time,first_time,assbool
    else:
      errmsg='the latest_item '+str(s.latest_item)+' and oldest_item '+str(s.oldest_item)
      errmsg+='have unaccounted for values. '
      raise TypeError(errmsg)
  def usr_languages(s):
    ''' Get a list of the languages the user understands. The indicator
    langcheck is 1 if the user has specified languages and 0 if not.

    :rtype: Bool, list of strings
    :returns: langcheck, languages'''
    usr=s.__get_user_item__()
    if not isinstance(usr['settings'],str):
      langcheck=False
      languages=list()
    else:
      settings=usr['settings']
      settings=settings.translate(str.maketrans('','',string.punctuation))
      languages=settings[1:]
      langcheck=True
    return langcheck, languages
  def usr_followers(s):
    ''' Get a list of the user_id's for the users this user follows.'''
    usr_fol_id=list()
    if not isinstance(s.__get_user_item__()['following'],str):
      return usr_fol_id
    fol_list=s.__get_user_item__()['following'].translate(str.maketrans('','',string.punctuation))
    return fol_list
  def item_valid(s,item_id,content_return,times,langcheck,languages,all_terms):
    ''' Determine whether the item given by `item_id' is valid for the users requested content.
    :param item_id: string index for the item in the content dataframe
    :param content_return: list of item_id's to be returned.
    :param times: [first_time,last_time] the time interval the content should be between.
    :param langcheck: indicator as to whether languages should be checked or not.
    :param languages: list of languages the user understands.
    :param all_terms: indicator if REJECTED items and items in non-readible language are to be included.

    If the item given by item_id is APPROVED; in a readible language, and occurs within the time frame
    then it's index is appended to the content to be returned and the valid indicator is set to TRUE.
    Else: content_return is unchanged and valid indicator is set to FALSE.

    :rtype: list of strings, Bool
    :returns: content_return, valid
    '''
    content=s.__get_content_csv__()
    valid=True # valid is initialised to True and is altered if any invalid conditions hold
    # When a False validity occurs the content_return id list and valid
    # are returned without the other checks as all need to be True for the item to be stored.
    if all_terms:
      t=s.__content_time__(item_id)
      if not times[0]>=t>=times[1]:
        valid=False
        return content_return,valid
    else:
      if langcheck:
        lang=content.loc[item_id]['language']
        if lang is None:
          valid=False
          return content_return,valid
        if not lang in languages:
          valid=False
          return content_return,valid
      if not 'APPROVED' in content.loc[item_id][1]:
        valid=False
        return content_return,valid
    t=s.__content_time__(item_id)
    print(type(times[0]),type(t))
    if not times[0]>=t>=times[1]:
      valid=False
      return content_return,valid
    if valid:
      content_return.append(item_id)
    return content_return,valid
  def content_request(s,n_items=0,all_terms=0):
    ''' Return n_items of all approved content from the latest_term going newer or olderest_term getting older.
    If all_terms is one then also include rejected terms.
    Only terms which are in the users available language are included.
    :param n_items: integer number of terms requested. If n_items is None then all new terms are returned
    :param all_terms: default to 0, if 1 then include rejected terms, else invalid.

    :rtype: data_frame
    :returns: data_frame of the new content'''
    if not (all_terms==0 or all_terms==1):
      print('all_terms takes invalid value, should be 0 or 1 but instead is '+str(all_terms))
    if n_items is None or n_items<0:
      # If n_items is None then all new terms should be returned, the
      # max n_terms is therefore the row number of the latest_item
      n_items=s.number_of_terms()
    elif isinstance(n_items, (float,str)):
      n_items=int(n_items)
    print(n_items) #FIXME
    if n_items==0:
      print('No content requested')
      return
    else:
      content=s.__get_content_csv__()
      content_return   =list()
      content_return_pr=list() # Priority list based on followers.
      # Use pivot_terms to determine whether newer or older content is being found.
      piv1,last_time,first_time,assbool=s.pivot_terms()
      times=[first_time,last_time]
      if last_time is None and first_time is None:
        # If neither old or new is determined then return all approved content is a viable language.
        return s.apprv_content()
      # Reorder the content so that either the latest_item is above new or oldest_item above older.
      content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")
      content=content.sort_values(by='created',axis=0,ascending=assbool)
      piv2=content.index[-1]
      # Locate the pivot term for searching
      r1=content.index.get_loc(piv1)
      r2=content.index.get_loc(piv2)
      langcheck,languages=s.usr_languages()
      # iterate through the possible terms, stop once n_terms are reached or the terms run out.
      usr_fol_list=s.usr_followers()
      for c in range(r1,r2):
        item_id=content.index[c]
        usr_crt=content.loc[item_id]['uploader_user_id']
        if not isinstance(usr_crt,str):
          prior=False
        elif len(usr_crt)<=1:
          prior=False
        else:
          prior=usr_crt in usr_fol_list
        #print(prior,usr_crt)
        if prior:
          content_return_pr,valid=s.item_valid(item_id,content_return_pr,times,langcheck,languages,all_terms)
        else:
          content_return,valid=s.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
        if len(content_return_pr)>=n_items:
          break
      np=len(content_return_pr)
      print(np,'number of priority terms',content_return_pr) #FIXME
      content_return_pr+=content_return[0:n_items-np]
      if len(content_return_pr)==0:
        return(content.iloc[r1])
      else:
        return content.loc[content_return_pr]
  def apprv_content(s,all_terms=0):
    ''' Return a data_frame containing only the approved content'''
    content=s.__get_content_csv__()
    content_return=list()
    langcheck,languages=s.usr_languages()
    times=[content['created'].min(skipna=True),content['created'].max(skipna=True)]
    print('apprv',times) #FIXME
    for c in content.index:
      content_return,valid=s.item_valid(c,content_return,times,langcheck,languages,all_terms)
    return content.loc[content_return]
  def number_of_terms(s):
    content=s.__get_content_csv__()
    return content.shape[0]


if __name__=='__main__':
  print('Running  on python version')
  print(sys.version)
  content=pd.read_csv('content.csv',index_col=1)
  n_terms=content.shape[0]
  latest_item=content.index[int(n_terms/2)]
  users=pd.read_csv('users.csv',index_col=1)
  N=len(users.index)
  r=random.randint(0,N)
  user_id=users.index[r]
  UC=UserContent(user_id=user_id,latest_item=latest_item)
  PSN_tests.tests(UC)
  exit()

