#import modules
import pandas as pd
import IPython as ipy

#import group chat csv
group_chat = pd.read_csv('~/Library/Messages/group_chat.csv')

#remove duplicated texts, there are 3 copies of each message
group_chat = group_chat.loc[~group_chat.duplicated(keep='last')]

#remove columns other than text and handle_id (sender)
group_chat = group_chat.loc[:, ['text', 'handle_id']].rename(columns={'handle_id' : 'sender'})

#map handle_ids to member 
group_chat.sender.loc[group_chat.sender == '0'] = 'PersonA'
group_chat.sender.loc[group_chat.sender == '1275'] = 'PersonB'
group_chat.sender.loc[group_chat.sender == '1315'] = 'PersonC'
group_chat.sender.loc[group_chat.sender == '1324'] = 'PersonD'
group_chat.sender.loc[group_chat.sender == '1428'] = 'PersonE'

#total amount of texts
texts_total = len(group_chat)

#creates new column that is first word of each text
group_chat['reaction'] = group_chat.text.str.split(' ').str.get(0)

#creates new column that is the text reacted to (doesn't include "REACTED TO", split based on “ not ")
group_chat['reacted_text'] = group_chat.text.str.split('“').str.get(1).str[:-1]

#all reactions
reactions = ['Loved', 'Liked', 'Disliked', 'Laughed', 'Emphasized', 'Questioned']

#new dataframe that only contains reaction texts
reaction_messages = group_chat.loc[group_chat.reaction.isin(reactions)]

#lists of indexes and reacted texts for all reaction messages
popular_messages_index = list(reaction_messages.index)
popular_messages_text = list(reaction_messages.reacted_text)

#this loop will remove items if it's the same reacted text, but have to make sure indexes are far apart, or else it could be same text getting reacted to at different points.
for ii in range(len(reaction_messages)):

    index = popular_messages_index[ii]

    if ii > 0 and ii < len(popular_messages_index) - 1:
        pass

#initalize dataframe to add to
popular_excerpts = pd.DataFrame()

#for each item, grab the previous ten texts to give the context for the conversation
for item in popular_messages_index:

     excerpt = group_chat.loc[item-10:item, :]
     popular_excerpts = pd.concat([popular_excerpts, excerpt])

#export dataframe that contains popular excerpts
popular_excerpts.to_csv('popular_excerpts.csv')
