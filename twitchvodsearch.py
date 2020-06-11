'''
Twitch VOD Search -- A tool to view chatlogs from VODs
and find comments mentioning specific keywords.

by thisismy-github, 4/5/20

TODO:
    -add emoji support for exporting data to files
    -allow users to get VODs from specific timeframes
    -allow users to search for messages from specific users
    -integrate this into a webapp to host on the website
    -make this into a class?
    -bugfixing
'''

from twitch import Helix
import re, time, argparse

# --- API key ---
helix = Helix(client_id='abiqngxwr5p4wovuabpye4o27ua4zs',
              client_secret='ik8r0mghsfvddg43zc62wsc6ve5sio',
              bearer_token='kk5ea0zzu6qn7a5w7yf60sylmev5on',
              use_cache=True)

# --- Argument parser ---
parser = argparse.ArgumentParser(description="View VOD comments and search through them.")
parser.add_argument("-u", "--user", help="desired user to view")
parser.add_argument("-c", "--count", help="number of most recent vods to view", type=int, default=1)
parser.add_argument("-s", "--search", help="term to search for in vods")
parser.add_argument("-t", "--realtime", help="include real-world time comments were posted at", action="store_true")
args = parser.parse_args()

# --- Main stuff ---
user = helix.user(args.user if args.user else input('User: '))
vodCount = args.count if args.search else int(input('Number of VODs to search: '))
vods = user.videos(first=vodCount)
searchTerm = args.search if args.search else input('Search for: ')
showRealTime = args.realtime


def viewVod(vod, searchTerm=searchTerm, showRealTime=showRealTime):
    print('-'*60)
    print(vod)
    print('-'*60)
    totalComments = 0
    if searchTerm:
        totalComments = 0
        for c in vod.comments:
            if re.search(searchTerm, c.message.body):
                totalComments += 1
                timestamp = time.strftime('%H:%M:%S', time.gmtime(c.content_offset_seconds))
                if showRealTime: timestamp += f", {c.commenter.created_at}"
                print(c.commenter.name, timestamp,'\n     ',c.message.body,'\n')
        print(f'Total comments with the keyword "{searchTerm}": {totalComments}')
    else:
        for c in vod.comments:
            totalComments += 1
            timestamp = time.strftime('%H:%M:%S', time.gmtime(c.content_offset_seconds))
            if showRealTime: timestamp += f", {c.commenter.created_at}"
            print(c.commenter.name, timestamp,'\n     ',c.message.body,'\n')
        print(f'Total comments: {totalComments}')


if vodCount == -2:
    print(user.data['id'])
else:
    for vod in vods:
        viewVod(vod, searchTerm)
input('\nPress enter to quit.')