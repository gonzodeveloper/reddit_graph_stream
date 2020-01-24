from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import praw
import pandas as pd
import sys


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_yaml", type=str, required=True,
                        help="path to config yml specifying reddit client info")
    parser.add_argument("--target", type=str, required=True,
                        help="sub reddit you wish to scrape")
    parser.add_argument("--output", type=str, required=True,
                        help="output file")
    parser.add_argument("-n", "--num_submissions", type=, required=True,
                        help="number of submissions to analyze")

    args = parser.parse_args()

    # Open YAML config
    with open(args.config_yaml, "r") as config_file:
        config = yaml.load(config_file)

    # Get Reddit Client
    reddit = praw.Reddit(client_id=config['client_id'],
                         client_secret=config['client_secret'],
                         username=config['username'],
                         password=config['password'],
                         user_agent=config['user_agent'])

    # Get subreddit
    subreddit = reddit.subreddit(args.target)

    # VADER Sentiment analyzer http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf
    analyser = SentimentIntensityAnalyzer()
    
    posts = []

    # Notice how this gets "hot" submissions, you can also search for historical!
    for idx, submission in enumerate(subreddit.hot(limit=args.num_submissions))):
        print("Reading Submissions: {}".format(idx + 1), end="\r")
        
        # Ignore sticky submissions (usually rules threads)
        if not submission.stickied:
            # Update "comment forest" 
            submission.comments.replace_more(limit=24)
            
            # Get all comments under the submission
            for comment in submission.comments.list():

                if comment.body is not None:
                    # Get VADER Compound score
                    score = analyser.polarity_scores(comment.body)['compound']
                    posts.append([comment.ups, score])


    print()
    df = pd.DataFrame(posts, columns=['comment_ups', 'compound_score'])
    df.to_csv(args.output, header=True, index=False)

