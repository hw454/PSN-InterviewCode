import PSN_CodeChallenge
import pandas as pd
import random

'''
test1:  No inputs
test2:  Return all content
test3:  Return only the newest content (approved and rejected)
test4:  For random "latest_item" and n_items=None test all content terms are APPROVED.
test4b: For random "latest_item" and n_items=randint test all content terms are APPROVED.
test5:  n_items is negative
test6:  n_items is bigger than the number of content terms
test7:  n_items is a float
test8:  n_items is a string
test9:  latest_item=None
test10: Return only the Approved content
test11: Detect if oldest_item and latest_item are both set
test12: For random "oldest_item"
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
  n_items=random.randint(0,UC.number_of_terms()-1)
  test3out=UC.content_request(n_items,all_terms=1)
  if shape_test(test3out,n_items):
    return True
  else:
    print('failed to return the new content including rejected items')
    return False

def test4(UC):
  ''' Randomly choose the latest term then check all new items are returned '''
  maxn_items=UC.number_of_terms()-1
  nAve=5
  n_items=None
  for i in range(nAve):
    rand_lat_num=random.randint(0,maxn_items)
    UC.latest_item=UC.id_from_row_num(rand_lat_num)
    output_df=UC.content_request(n_items)
    if appr_test(output_df):
      continue
    else:
      print('Test failed for n_items None and latest_item in row %d'%rand_lat_num)
      return False
  return True

def test4b(UC):
  ''' Randomly choose the latest term then check all new items are returned '''
  maxn_items=UC.number_of_terms()-1
  nAve=5
  for i in range(nAve):
    rand_lat_num=random.randint(0,maxn_items)
    n_items=random.randint(0,rand_lat_num)
    UC.latest_item=UC.id_from_row_num(rand_lat_num)
    output_df=UC.content_request(n_items)
    if appr_test(output_df):
      continue
    else:
      print('Test failed for n_items rand %d and latest_item rand in row %d'%(n_items,rand_lat_num))
      return False
  return True

def test5(UC):
  ''' The request n_items is negative, then find all new terms'''
  n_items=-random.randint(0,UC.number_of_terms()-1)
  test5out=UC.content_request(n_items)
  if  appr_test(test5out):
    return True
  else:
    print('test for n_items negative failed')
    return False
  return True

def test5b(UC):
  '''If the latest_item is None and n_items is negative then all approved items should be returned'''
  n_items=-random.randint(0,UC.number_of_terms()-1)
  UC.latest_item=None
  test5out=UC.content_request(n_items)
  apprv_df=UC.apprv_content()
  if  appr_test(test5out) and test5out.equals(apprv_df):
    return True
  else:
    print('test for n_items negative failed')
    return False

def test6(UC):
  ''' The requested n_items is more than the content terms so all new terms should be found '''
  n_items=random.randint(UC.number_of_terms(),2*UC.number_of_terms())
  test6out=UC.content_request(n_items)
  apprv_df=UC.apprv_content()
  if  appr_test(test6out) and apprv_df.equals(test6out):
    return True
  else:
    print(apprv_df.equals(test6out))
    print(apprv_df,test6out)
    print('test for n_items bigger than content failed')
    return False

def test7(UC):
  ''' The requested n_items is a float type variable. '''
  n_items=random.rand(0,UC.number_of_terms(),0.25)
  test7out=UC.content_request(n_items)
  if  appr_test(test7out) and shape_test(test7out,int(n_items)):
    return True
  else:
    print('test for n_items a float failed')
    return False

def test8(UC):
  ''' The requested n_items is a string type variable. '''
  n_items=str(random.rand(0,UC.number_of_terms()))
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
  n_items=5
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

def test12(UC):
  ''' Randomly choose the oldest term then check all new items are returned '''
  maxn_items=UC.number_of_terms()-1
  n_items=random.randint(0,maxn_times)
  rand_lat_num=random.randint(0,maxn_items)
  rand_old_num=random.randint(0,maxn_items)
  UC.latest_item=UC.id_from_row_num(rand_lat_num)
  UC.oldest_item=UC.id_from_row_num(rand_old_num)
  output_df=UC.content_request(n_items)
  if appr_test(output_df):
    print('Test failed to detect both oldest '+str(s.oldest_item)+' and latest item '+str(s.latest_item)+'were set')
    return False
  else:
    return True

def test12(UC):
  ''' Randomly choose the oldest term then check all new items are returned '''
  maxn_items=UC.number_of_terms()-1
  nAve=5
  n_items=None
  for i in range(nAve):
    rand_lat_num=random.randint(0,maxn_items)
    UC.oldest_item=UC.id_from_row_num(rand_lat_num)
    output_df=UC.content_request(n_items)
    if appr_test(output_df):
      continue
    else:
      print('Test failed for n_items None and latest_item in row %d'%rand_lat_num)
      return False
  return True

def test12b(UC):
  ''' Randomly choose the oldest term then check all new items are returned '''
  maxn_items=UC.number_of_terms()-1
  nAve=5
  for i in range(nAve):
    rand_lat_num=random.randint(0,maxn_items)
    n_items=random.randint(0,rand_lat_num)
    UC.oldest_item=UC.id_from_row_num(rand_lat_num)
    output_df=UC.content_request(n_items)
    if appr_test(output_df) and shape_test(output_df,n_items):
      continue
    else:
      print('Test failed for n_items rand %d and oldest_item rand in row %d'%(n_items,rand_lat_num))
      return False
  return True

def shape_test(output_df,n_items):
  ''' test that the output data_frame has the correct shape
  :param output_df: the data_frame being tested
  :param n_items:   the number of items that should be in the data_frame

  :rtype: bool
  :returns: True if shape is correct, False if not
  '''
  if output_df.shape[0]==n_items and output_df.shape[1]==df_cols:
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
  if output_df.shape[0]==0:
    return True
  for ind in output_df.index:
    if any(term=='APPROVED' for term in output_df.loc[ind]):
      continue
    else: return False
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
  if not test4(UC):
    return False
  if not test4b(UC):
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
  if not test12(UC):
    return False
  if not test12b(UC):
    return False
  print('All tests passed')
  return True

if __name__=='__main__':
  UC=PSN_CodeChallenge.UserContent()
  tests(UC)
  exit()



