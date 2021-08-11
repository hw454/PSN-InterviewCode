# PSN-InterviewCode

The code in this repository is written to read and return items in a csv file. This is done using the object UserContent created in PSN_CodeChallenge.

To return the latest content for a user define the user_id and latest_item and enter these on contractuion of a UserContent object.
UC=UserContent(user_id=user_id,latest_item=latest_item) (*)
Then set the number of terms you want to request and request the items.
output=UC.content_request(n_items) (**)

If the latest_item is more than a day old then newer content will be returned.

Content from user's that the user follows will be prioritised. 

Only items in a language the user can read will be output unless the user has set no languages. 

Only APPROVED content will be returned.

If you desire older content then set the oldest_item and set latest_item to None. Then repeat (*) (**) replacing these terms.

If the latest_item or oldest_item are not set then the newest items will be returned. 

If the latest_item and oldest_item are not set and n_items is not set or invalid then all APPROVED terms in a suitable language will be returned.

If you want to include REJECTED and PENDING contents then set all_terms=1 and enter this in the content request as,
output=UC.content_request(n_items,all_terms)

To test all the functions run: python PSN_tests()
