import praw
import sys

def main(headfile, donefile):
	user_agent = "comment scraper for private subreddit for class: /u/miscalc"
	r = praw.Reddit(user_agent=user_agent)
	r.login('miscalc', 'MY PASSWORD GOES HERE')

	comments = []
	new_ids = []

	with open(donefile, 'r') as fread:
		already_done = fread.read().split('\n')

	private_subreddit = r.get_subreddit('NetworkCultures16')

	while True:
		submissions = private_subreddit.get_hot(limit=50)
		for submission in submissions:
			if submission.title[:5] == "[Week":
				print "Accessing Thread ", submission.title
				sub_comments = submission.comments
				flat_comments = praw.helpers.flatten_tree(sub_comments)
				for comment in flat_comments:
					if comment.id not in already_done:
						new_ids.append(comment.id)
						if comment.author_flair_text:
							comments.append(comment.author_flair_text.encode('utf-8') + ': \n' + comment.body.encode('utf-8'))
						else:
							comments.append(comment.body.encode('utf-8'))
		print "Added " + str(len(new_ids)) + " new responses"
		with open(headfile, 'a') as fopen:
			fopen.write('\n\n'.join(comments))
		with open(donefile, 'a') as fopen2:
			fopen2.write('\n'.join(new_ids))
		new_ids = []
		time.sleep(3600)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])