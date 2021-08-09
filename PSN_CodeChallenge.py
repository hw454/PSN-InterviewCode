#!/usr/bin/env python3
import pandas as pd
import sys
import datetime as dt
import PSN_tests

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
    return content
  def __getitem_with_row__(s,i):
    '''get the itemfor the 'ith' content term'''
    content=pd.read_csv(s.filename) # Returns a comma separated data frame from the CSV file.
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
  def __set_latest_item__(s,latest_item): s.latest_item=latest_item
  def __set_oldest_item__(s,oldest_item): s.oldest_item=oldest_item
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
    datetime_obj=dt.datetime.strptime(datetime_str,"%Y-%m-%d %H:%M:%S.%f")
    return datetime_obj
  def row_num_from_id(s,item_id):
    content=s.__get_content_csv__()
    row=content.loc[item_id][0]
    return row
  def id_from_row_num(s,r):
    item=s.__getitem_with_row__(r)
    item_id=item[1]
    return item_id
  def content_request(s,n_items=0,all_terms=0):
    ''' Return n_items of all approved content upto the latest_term, whichever is achieved first.
    If all_terms if one then also include rejected terms.
    :param n_items: integer number of terms requested. If n_items is None then all new terms are returned
    :param all_terms: default to 0, if 1 then include rejected terms, else invalid.

    :rtype: data_frame
    :returns: data_frame of the new content'''
    if not (all_terms==0 or all_terms==1):
      print('all_terms takes invalid value, should be 0 or 1 but instead is '+str(all_terms))
    if n_items is None or n_items<0:
      # If n_items is None then all new terms should be returned, the
      # max n_terms is therefore the row number of the latest_item
      n_items=s.row_num_from_id(s.latest_item)
    elif not isinstance(n_items, int):
      n_items=int(n_items)
    if n_items==0:
      print('No content requested')
      return
    else:
      content=s.__get_content_csv__()
      content_return=list()
      if s.latest_item is None:
        # since there is no lastest_item set the last_time to be the final content time.
        last_time=s.__content_time__(content.index[-1])
      else:
        # When latest_item is definded the last_time is the time of this item. No older items should be returned.
        last_time=s.__content_time__(s.latest_item)
      for c in content.index:
        t=s.__content_time__(c)
        if len(content_return)<n_items and t>=last_time:
          if content.loc[c][1]=='APPROVED' and all_terms==0:
            content_return.append(c)
          elif all_terms==1:
            content_return.append(c)
          else: continue # Loop should not be ended but term is invalid so not returned.
        else: break
      return content.loc[content_return]
  def apprv_content(s):
    ''' Return a data_frame containing only the approved content'''
    content=s.__get_content_csv__()
    content_return=list()
    for c in content.index:
      if content.loc[c][1]=='APPROVED':
        content_return.append(c)
      else: continue # Term is invalid so not returned.
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
  UC=UserContent(latest_item=latest_item)
  PSN_tests.tests(UC)
  exit()

