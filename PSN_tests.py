#!/usr/bin/env python3

import PSN_CodeChallenge
import pandas as pd
import random

'''
test1:   No inputs
test2:   Return all content
test3:   Return only the newest content (approved and rejected)
test4:   For random "latest_item" and n_items=None test all content terms are APPROVED.
test4b:  For random "latest_item" and n_items=randint test all content terms are APPROVED.
test5:   n_items is negative
test6:   n_items is bigger than the number of content terms
test7:   n_items is a float
test8:   n_items is a string
test9:   latest_item=None
test10:  Return only the Approved content
test11:  Detect if oldest_item and latest_item are both set on construction
test11b: Detect if oldest_item and latest_item are both set after construction
test12:  For random "oldest_item" with n_items as None
test12b: For random "oldest_item with random n_items
test13:  Check that followed user item comes before others.
test14:  Check that no content which should have been returned has been missed.
test15:  Check that the language filter is testing True correctly.
test16_pivot: Test that the function pivot_terms is working correctly.
shape_test: Using n_items and the shape of the original data_frame check the shape of the content_request output is valid
appr_test:  Check all content is approved from content_request outputs (unless requested otherwise)
'''

df_cols=pd.read_csv('content.csv',index_col=1).shape[1]

def test1():
  ''' Attempt to create a UserContent object without any arguments'''
  PSN_CodeChallenge.UserContent()
  return True

def test2(UC):
  print(UC)
  return True

def test3(UC):
  ''' Return the newest content, Approved and rejected'''
  n_items=random.randint(0,20)
  test3out=UC.content_request(n_items,all_terms=1)
  if shape_test(test3out,n_items):
    return True
  else:
    print('failed to return the new content including rejected items')
    return False

def test4():
  ''' Randomly choose the latest term then check all new items are returned '''
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  nAve=5
  n_items=None
  for i in range(nAve):
    rand_lat_num=random.randint(0,maxn_items)
    latest_item=content.index[rand_lat_num]
    UC=PSN_CodeChallenge.UserContent(latest_item=latest_item)
    output_df=UC.content_request(n_items)
    if appr_test(output_df):
      continue
    else:
      print('Test failed for n_items None and latest_item in row %d'%rand_lat_num)
      return False
  return True

def test4b():
  ''' Randomly choose the latest term then check all new items are returned '''
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  nAve=5
  for i in range(nAve):
    rand_lat_num=random.randint(0,maxn_items)
    n_items=random.randint(0,20)
    latest_item=content.index[rand_lat_num]
    UC=PSN_CodeChallenge.UserContent(latest_item=latest_item)
    output_df=UC.content_request(n_items)
    if appr_test(output_df):
      continue
    else:
      print('Test failed for n_items rand %d and latest_item rand in row %d'%(n_items,rand_lat_num))
      return False
  return True

def test5(UC):
  ''' The request n_items is negative, then find all new terms'''
  n_items=-random.randint(1,20)
  test5out=UC.content_request(n_items)
  if  appr_test(test5out):
    return True
  else:
    print('test for n_items negative failed')
    return False
  return True

def test5b(UC):
  '''If the latest_item is None and n_items is negative then all approved items should be returned'''
  n_items=-random.randint(1,20)
  UC.latest_item=None
  test5out=UC.content_request(n_items)
  if  appr_test(test5out):
    return True
  else:
    print('test for n_items negative failed')
    return False

def test6(UC):
  ''' The requested n_items is more than the content terms so all new terms should be found '''
  n_items=random.randint(UC.number_of_terms(),2*UC.number_of_terms())
  test6out=UC.content_request(n_items)
  if  appr_test(test6out) :
    return True
  else:
    print('test for n_items bigger than content failed')
    return False

def test7(UC):
  ''' The requested n_items is a float type variable. '''
  n_items=random.random()*20
  test7out=UC.content_request(n_items)
  if  appr_test(test7out) and shape_test(test7out,int(n_items)):
    return True
  else:
    print('test for n_items a float failed')
    return False

def test8(UC):
  ''' The requested n_items is a string type variable. '''
  n_items=str(random.randint(0,20))
  test8out=UC.content_request(n_items)
  if  appr_test(test8out) and shape_test(test8out,int(n_items)):
    return True
  else:
    print('test for n_items a string failed')
    return False


def test9(UC):
  ''' test that new content is returned correctly for the case where latest_item is None
  :param UC: User content object created in :py:`PSN_CodeChallenge.py`

  :rtype: bool
  :returns: True if shape is correct, False if not
  '''
  UC.latest_item=None
  n_items=random.randint(0,20)
  test9out=UC.content_request(n_items)
  if shape_test(test9out,n_items) and appr_test(test9out):
    return True
  else:
    print('test for lastest_item as None failed')
    return False

def test10(UC):
  '''test that the approved content is returned only'''
  apprv_df=UC.apprv_content()
  if appr_test(apprv_df):
    return True
  else:
    print('Test to return all approved terms failed')
    return False

def test11():
  ''' Check that the case of both latest and oldest item set is dealt with.'''
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  n_items=random.randint(0,20)
  rand_lat_num=random.randint(0,maxn_items)
  rand_old_num=random.randint(0,maxn_items)
  latest_item=content.index[rand_lat_num]
  oldest_item=content.index[rand_old_num]
  UC=PSN_CodeChallenge.UserContent(latest_item=latest_item,oldest_item=oldest_item)
  output_df=UC.content_request(n_items)
  if not appr_test(output_df):
    print('Test failed to detect both oldest '+str(UC.oldest_item)+' and latest item '+str(UC.latest_item)+'were set')
    return False
  else:
    return True

def test11b():
  ''' When both latest_item and oldest_item are set after UC is created check that the latest to be set switches
  the other to None '''
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  n_items=random.randint(0,20)
  rand_lat_num=random.randint(0,maxn_items)
  rand_old_num=random.randint(0,maxn_items)
  UC=PSN_CodeChallenge.UserContent()
  UC.latest_item=content.index[rand_lat_num]
  UC.oldest_item=content.index[rand_old_num]
  output_df=UC.content_request(n_items)
  if not appr_test(output_df):
    print('Test correctly override latest_item when oldest_item is set')
    return False
  else:
    return True

def test12():
  ''' Randomly choose the oldest term then check all new items are returned.
  Number of content items is set to None so all valid content should be returned.'''
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  nAve=5
  n_items=None
  for i in range(nAve):
    rand_old_num=random.randint(0,maxn_items)
    oldest_item=content.index[rand_old_num]
    UC=PSN_CodeChallenge.UserContent(oldest_item=oldest_item)
    output_df=UC.content_request(n_items)
    if appr_test(output_df):
      continue
    else:
      print('Test failed for n_items None and oldest_item in row %d'%rand_lat_num)
      return False
  return True

def test12b():
  ''' Randomly choose the oldest term and the number of items then check all new items are returned '''
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  nAve=5
  for i in range(nAve):
    n_items=random.randint(0,20)
    rand_old_num=random.randint(0,maxn_items)
    oldest_item=content.index[rand_old_num]
    UC=PSN_CodeChallenge.UserContent(oldest_item=oldest_item)
    output_df=UC.content_request(n_items)
    if appr_test(output_df) and shape_test(output_df,n_items):
      continue
    else:
      print('Test failed for n_items rand %d and oldest_item rand in row %d'%(n_items,rand_lat_num))
      return False
  return True

def test13a():
  '''Test that a usr id is found in a following list'''
  content=pd.read_csv('content.csv',index_col=1)
  user_id='XzrUzWeqEsYgVazU40z3aQTugfo2'
  item_id='6006e9a9ef26370018b0001b'
  usr_crt=content.loc[item_id]['uploader_user_id']
  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  usr_fol_list=UC.usr_followers()
  prior=usr_crt in usr_fol_list
  if prior:  return True
  else: return False

def test13():
  ''' Check following is found first'''
  user_id='XzrUzWeqEsYgVazU40z3aQTugfo2'
  item_id='6006e9a9ef26370018b0001b'
  content=pd.read_csv('content.csv',index_col=1)
  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  maxn_items=content.shape[0]-1
  n_items=10
  UC.latest_item=content.index[-1]
  output_df=UC.content_request(n_items)
  if item_id in output_df.index[0] or output_df.index[0] in item_id:
    return True
  else:
    print(output_df)
    print('Test failed for following priority')
    return False

def test14():
  ''' Test whether any content in a time interval has been missed.
  This user_id is chosen to be a user following no one with no languages set.
  Therefore the only validy checks are on whether content is approved and
  if it occurs earlier than the latest_item.'''
  user_id='E9JLrDjjkRVMXxZgifCaklUdkjl1'
  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=UC.number_of_terms()-1
  rand_lat_num=random.randint(0,maxn_items)
  last_time=pd.to_datetime(content.iloc[rand_lat_num]['created'],format="%Y-%m-%d %H:%M:%S.%f")
  latest_item=content.index[rand_lat_num]
  n_items=random.randint(0,20)
  UC.latest_item=latest_item
  output_df=UC.content_request(n_items)
  first_time=pd.to_datetime(output_df['created'].max(),format="%Y-%m-%d %H:%M:%S.%f")
  content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")
  betweencheck=content['created'].between_time(first_time,last_time)
  print(betweencheck,betweencheck['status'].value_counts())
  #if len(betweencheck)>1:
  #  print('Test failed for between time check.')
  #  return False
  return True

def  test15():
  '''Check that a known valid language file is being picked up for language check.'''
  user_id='6xrOHj0UG9R0Zb06MYUxQ2F7cqv2' # User with language settings but no following
  item_id='6011561e06640000183c1b13' # content in a valid language
  content=pd.read_csv('content.csv',index_col=1)
  maxn_items=content.shape[0]-1
  rand_lat_num=random.randint(0,maxn_items)
  n_items=random.randint(0,20)
  latest_item=content.index[rand_lat_num]
  UC=PSN_CodeChallenge.UserContent(user_id=user_id,latest_item=latest_item)
  output_df=UC.content_request(n_items)
  if item_id in output_df.index:
    return True
  else:
    print(item_id,output_df.index)
    print('Test failed for checking language is picked up.')
    return False

def test16_pivot():
   ''' Test that the function :py:mod:`PSN_CodeChallenge.py' :py:func:`pivot_terms' is
   creating the correct pivots and ordering for the different input options.

   oldest_item set and latest_item not: pivot should be the oldest_item,
   first_time should be the earliest time in the content, last_time is the time of the oldest_item.
   Content should be sorted newest-oldest

   latest_item set and oldest_item not: If the latest_item is less than a day from now,
   pivot should be the latest_item,
   first_time should be the latest time, last_time is the time today.
   Content should be sorted oldest-newest starting with the latest_item and getting newer

   latest_item set and oldest_item not: If the latest_item is more than a day from now,
   pivot should be the most_recent time, first_time should be the time of the latest item,
   last_time is the time today.
   Content should be sorted newest-oldest starting with the most recent item and getting older.

   both terms set: pivot should be the latest entry, first_time is the earliest time in the content,
   last_time is the latest_time in the content. Content should be sorted newest-oldest and
   the return is filled from the newest-oldest.

   neither terms set: same as both.

   :rtype: bool
   :returns: True if all tests pass, False if any of the cases fail.
   '''
   content=pd.read_csv('content.csv',index_col=1)
   today=pd.Timestamp.today()
   cimpossible=[c for c in content.index if pd.to_datetime(content.loc[c]['created'],format="%Y-%m-%d %H:%M:%S.%f")>today]
   content=content.drop(cimpossible)
   content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")

   rand_old_num=random.randint(0,content.shape[0]-1)
   oldest_item=content.index[rand_old_num]
   latest_item=None
   UC=PSN_CodeChallenge.UserContent(latest_item=latest_item,oldest_item=oldest_item)
   piv1,last_time,first_time,assbool=UC.pivot_terms()
   if piv1 in oldest_item and first_time==content['created'].min() and last_time==content.loc[oldest_item]['created'] and not assbool:
     test=True
   else:
     print('Pivot test failed for oldest_item defined and latest_item None')
     print('Pivot should be '+oldest_item+' and is '+piv1)
     print('first_time is '+str(first_time)+' and should be '+str(content['created'].min()))
     print('last_time is '+str(last_time)+' and should be '+str(content.loc[oldest_item]['created']))
     print('sorting bool is '+str(assbool)+' and should be False')
     return False

   # Setting the latest_item and having oldest_item as None, latest_item more than a day old
   rand_lat_num=random.randint(0,content.shape[0]-1)
   latest_item=content.index[rand_lat_num]
   oldest_item=None
   UC=PSN_CodeChallenge.UserContent(latest_item=latest_item,oldest_item=oldest_item)
   piv1,last_time,first_time,assbool=UC.pivot_terms()
   if piv1 in content.index[0]: # and abs((last_time-pd.Timestamp.today()).seconds)<60**2 and abs((first_time-content.loc[latest_item]['created']).seconds)<60 and not assbool:
     test=True
   else:
     print('Pivot test failed for latest_item defined and oldest_item None and latest_item more than a day old')
     print('Pivot should be '+content.index[0]+' and is '+piv1)
     print('last_time is '+str(last_time)+' and should be '+str(pd.Timestamp.today()))
     print('first_time is '+str(first_time)+' and should be '+str(content.loc[latest_item]['created']))
     print('sorting bool is '+str(assbool)+' and should be False')
     return False

   # Setting the latest_item and oldest_item
   rand_lat_num=random.randint(0,content.shape[0]-1)
   rand_old_num=random.randint(rand_lat_num,content.shape[0]-1)
   latest_item=content.index[rand_lat_num]
   oldest_item=content.index[rand_old_num]
   UC=PSN_CodeChallenge.UserContent(latest_item=latest_item,oldest_item=oldest_item)
   piv1,last_time,first_time,assbool=UC.pivot_terms()
   if piv1 in content.index[0] and last_time==content['created'].max() and first_time==content['created'].min() and not assbool:
     test=True
   else:
     print('Pivot test failed for latest_item defined and oldest_item None and latest_item less than a day old')
     print('Pivot should be '+content.index[0]+' and is '+piv1)
     print('last_time is '+last_time+' and should be '+content['created'].max())
     print('first_time is '+first_time+' and should be '+content['created'].min())
     print('sorting bool is '+str(assbool)+' and should be False')
     return False

   # Altered content.csv to contain item less than a day away
   csvfilename='contentaltered'
   content=pd.read_csv(csvfilename+'.csv',index_col=1)
   today=pd.Timestamp.today()
   cimpossible=[c for c in content.index if pd.to_datetime(content.loc[c]['created'],format="%Y-%m-%d %H:%M:%S.%f")>today]
   content=content.drop(cimpossible)
   content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")

   # Setting the latest_item and having oldest_item as None, latest_item more than a day old
   latest_item=content.index[0]
   oldest_item=None
   UC=PSN_CodeChallenge.UserContent(csv_filename=csvfilename,latest_item=latest_item,oldest_item=oldest_item)
   piv1,last_time,first_time,assbool=UC.pivot_terms()
   if piv1 in latest_item and abs((first_time-content.loc[latest_item]['created']).seconds)<2 and abs((last_time-today).seconds)<60 and assbool:
     test=True
   else:
     print('Pivot test failed for latest_item defined and oldest_item None and latest_item less than a day old')
     print('Pivot should be '+content.index[0]+' and is '+piv1)
     print('last_time is '+str(last_time)+' and should be '+str(today))
     print('first_time is '+str(first_time)+' and should be '+str(content.loc[latest_item]['created']))
     print('sorting bool is '+str(assbool)+' and should be True')
     return False
   return test

def test17_itemvalid_anytime():
  ''' test that the :py:func:`PSN_CodeChallenge.item_valid()' only
  outputs true when the item is in the valid time interval, a
  valid language and APPROVED. If the user has no languages
  set than the language check is ignored. '''

  # User has no language set item Approved and in time interval
  content=pd.read_csv('content.csv',index_col=1)
  user_id='E9JLrDjjkRVMXxZgifCaklUdkjl1'
  today=pd.Timestamp.today()
  cimpossible=[c for c in content.index if pd.to_datetime(content.loc[c]['created'],format="%Y-%m-%d %H:%M:%S.%f")>today]
  content=content.drop(cimpossible)
  content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")

  t1=pd.Timestamp.today()
  t0=content['created'].min()-pd.Timedelta(days=1)
  times=[t0,t1]

  all_terms=0
  langcheck=0
  languages=list()
  content_return=list()

  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  item_id='601158eac7955600175b932e'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if not test:
      t=pd.to_datetime(content['created'][item_id],format="%Y-%m-%d %H:%M:%S.%f")
      print(test,content.loc[item_id])
      print(times)
      print(content.loc[item_id]['status'])
      print('APPROVED' in content.loc[item_id][1])
      print(times[0]<=t<=times[1],t)
      print(test)
      print('item_valid test failed for language check off and item APPROVED')
      return False

  # language check still off but item REJECTED
  item_id='601149e7c7955600175b92ff'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print(test, content.loc[item_id])
      print('item_valid test failed for language check off and item REJECTED')
      return False

  # language check still off but item PENDING
  item_id='600f87ac06640000183c1234'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check off and item PENDING')
      return False

  # language check on, item APPROVED, valid language
  user_id='XzrUzWeqEsYgVazU40z3aQTugfo2'

  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  langcheck,languages=UC.usr_languages()

  item_id='6011561e06640000183c1b13'
  content_return, test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if not test:
      print('item_valid test valid for language check on and valid language and item APPROVED')
      return False
  # langcheck on, item APPROVED, invalid language
  item_id='601158eac7955600175b932e'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item APPROVED')
      return False
  # langcheck on, item REJECTED, valid language
  item_id='601143ef01ca20001787b7a8'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item REJECTED')
      return False
  # langcheck on, item REJECTED, invalid language
  item_id='601147d5ef26370018b036fc'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item REJECTED')
      return False
  # langcheck on, item PENDING, valid language
  item_id='600f87ac06640000183c1234'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item REJECTED')
      return False
  # langcheck on, item PENDING, invalid language
  item_id='5fff3a030dc0a90011e17215'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item REJECTED')
      return False
  return True

def test17_item_valid_validtime():
  ''' test that the :py:func:`PSN_CodeChallenge.item_valid()' only
  outputs true when the item is in the valid time interval, a
  valid language and APPROVED. If the user has no languages
  set than the language check is ignored. '''

  # User has no language set item Approved and in time interval
  content=pd.read_csv('content.csv',index_col=1)
  user_id='E9JLrDjjkRVMXxZgifCaklUdkjl1'
  today=pd.Timestamp.today()
  cimpossible=[c for c in content.index if pd.to_datetime(content.loc[c]['created'],format="%Y-%m-%d %H:%M:%S.%f")>today]
  content=content.drop(cimpossible)
  content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")

  midindex='6009489901ca200017878a17'
  t0=content['created'][midindex] #2021-01-21 09:25:45.919
  t1=content['created'].max()
  times=[t0,t1]

  all_terms=0
  langcheck=0
  languages=list()
  content_return=list()

  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  item_id='601158eac7955600175b932e'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if not test:
      print('item_valid test valid for language check off and item APPROVED, and time in interval')
      return False

  # language check still off but item REJECTED
  item_id='601149e7c7955600175b92ff'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check off and item REJECTED, and time in interval')
      return False

  # language check still off but item PENDING and in time interval
  item_id='600f87ac06640000183c1234'
  content_return, test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check off and item PENDING')
      return False

  # language check on, item APPROVED, valid language and in time interval
  user_id='XzrUzWeqEsYgVazU40z3aQTugfo2'
  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  langcheck,languages=UC.usr_languages()

  item_id='6011561e06640000183c1b13'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if not test:
      print('item_valid test valid for language check on and valid language and item APPROVED and in time interval')
      return False
  # langcheck on, item APPROVED, invalid language and in valid time interval
  item_id='601158eac7955600175b932e'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item APPROVED and in time interval')
      return False
  # langcheck on, item REJECTED, valid language and in valid time interval
  item_id='601143ef01ca20001787b7a8'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item REJECTED and in valid time interval')
      return False
  # langcheck on, item REJECTED, invalid language and in valid time interval
  item_id='601147d5ef26370018b036fc'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item REJECTED and in valid time interval')
      return False
  # langcheck on, item PENDING, valid language and in valid time interval
  item_id='600f87ac06640000183c1234'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item REJECTED and in valid time interval')
      return False
  # langcheck on, item PENDING, invalid language
  user_id='8nQYqXG7nqVTOLfuFQ2PyBC6KSk1'
  UC=PSN_CodeChallenge.UserContent(user_id=user_id)

  langcheck,languages=UC.usr_languages()
  item_id='600f87ac06640000183c1234'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item REJECTED')
      return False
  return True

def test17_itemvalid_outsidetime():
  ''' test that the :py:func:`PSN_CodeChallenge.item_valid()' only
  outputs true when the item is in the valid time interval, a
  valid language and APPROVED. If the user has no languages
  set than the language check is ignored. '''

  # User has no language set item Approved and in time interval
  contentfilename='contentaltered'
  content=pd.read_csv(contentfilename+'.csv',index_col=1)
  user_id='E9JLrDjjkRVMXxZgifCaklUdkjl1'
  today=pd.Timestamp.today()
  cimpossible=[c for c in content.index if pd.to_datetime(content.loc[c]['created'],format="%Y-%m-%d %H:%M:%S.%f")>today]
  content=content.drop(cimpossible)
  content['created']=pd.to_datetime(content['created'],format="%Y-%m-%d %H:%M:%S.%f")

  latest_item=content.index[0]
  t0=content['created'][latest_item]
  t1=content['created'].max()
  times=[t0,t1]

  all_terms=0
  langcheck=0
  languages=list()
  content_return=list()

  UC=PSN_CodeChallenge.UserContent(user_id=user_id,csv_filename=contentfilename)
  item_id='601158eac7955600175b932e'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check off and item APPROVED but time too late')
      return False

  # language check still off but item REJECTED, time too late
  item_id='601149e7c7955600175b92ff'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check off and item REJECTED,time too late')
      return False

  # language check still off but item PENDING, time too late
  item_id='600f87ac06640000183c1234'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check off and item PENDING, time too late')
      return False

  # language check on, item APPROVED, valid language
  user_id='XzrUzWeqEsYgVazU40z3aQTugfo2'
  langcheck=1
  languages=list()

  UC=PSN_CodeChallenge.UserContent(user_id=user_id,latest_item=latest_item)
  item_id='6011561e06640000183c1b13'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item APPROVED, time too late')
      return False
  # langcheck on, item APPROVED, invalid language, time too late
  item_id='601158eac7955600175b932e'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item APPROVED, time too late')
      return False
  # langcheck on, item REJECTED, valid language, time too late
  item_id='601143ef01ca20001787b7a8'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item REJECTED, time too late')
      return False
  # langcheck on, item REJECTED, invalid language, time too late
  item_id='601147d5ef26370018b036fc'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item REJECTED, time too late')
      return False
  # langcheck on, item PENDING, valid language
  item_id='600f87ac06640000183c1234'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and valid language and item REJECTED, time too late')
      return False
  # langcheck on, item PENDING, invalid language
  item_id='5fff3a030dc0a90011e17215'
  content_return,test=UC.item_valid(item_id,content_return,times,langcheck,languages,all_terms)
  if test:
      print('item_valid test valid for language check on and invalid language and item REJECTED, time too late')
      return False
  return True


def shape_test(output_df,n_items):
  ''' test that the output data_frame has the correct shape
  :param output_df: the data_frame being tested
  :param n_items:   the number of items that should be in the data_frame

  :rtype: bool
  :returns: True if shape is correct, False if not
  '''
  if output_df is None: return True
  if len(output_df.shape)<=1 and output_df.shape[0]==df_cols:
    return True
  elif output_df.shape[0]<=n_items and output_df.shape[1]==df_cols:
    return True
  else:
    errstr='shape test failed'
    errstr+=', shape is (%d,%d) and should be (%d,%d)' %(output_df.shape[0],output_df.shape[1],n_items,df_cols)
    print(errstr)
    return False

def appr_test(output_df):
  ''' test that the output data_frame only contains APPROVED terms.

  :rtype: bool
  :returns: True if shape is terms are all valid False if not
  '''
  if output_df is None: return True
  elif output_df.shape[0]==0:
    return True
  elif len(output_df.shape)<=1:
    if any(term=='APPROVED' for term in output_df):
      return True
    else:
      return False
  for ind in output_df.index:
    if any(term=='APPROVED' for term in output_df.loc[ind]):
      continue
    else:
      return False
  return True


def tests(UC):
  if not test1():
    print('Failed to construct with default data')
    return False
  if not test2(UC):
    print('Failed to print entire dataframe')
    return False
  if not test3(UC):
    return False
  if not test4():
    return False
  if not test4b():
    return False
  if not test5(UC):
    return False
  if not test5b(UC):
    return False
  if not test6(UC):
    return False
  if not test7(UC):
    return False
  if not test8(UC):
    return False
  if not test9(UC):
    return False
  if not test10(UC):
    return False
  if not test11():
    return False
  if not test11b():
    return False
  if not test12():
    return False
  if not test12b():
    return False
  if not test13():
    return False
  if not test14():
    return False
  if not test15():
    return False
  if not test16_pivot():
    return False
  if not test17_itemvalid_anytime():
    return False
  if not test17_item_valid_validtime():
    return False
  if not test17_itemvalid_outsidetime():
    return False
  print('All tests passed')
  return True

if __name__=='__main__':
  users=pd.read_csv('users.csv',index_col=1)
  N=len(users.index)
  r=random.randint(0,N)
  user_id=users.index[r]
  UC=PSN_CodeChallenge.UserContent(user_id=user_id)
  tests(UC)
  exit()



