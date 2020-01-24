import praw
import argparse
import yaml

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--config_yaml", type=str, required=True,
                        help="path to config yml specifying reddit client info")
    parser.add_argument("--target", type=str, required=True,
                        help="sub reddit you wish to scrape")
    parser.add_argument("--output", type=str, required=True,
                        help="outputfile")

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

    # Open file to append too
    with open(args.output, "a") as output:

        # Stream comments until user decides otherwise
        for idx, comment in enumerate(subreddit.stream.comments()):
            try:
                print("Streaming Comments...{}".format(idx), end="\r")
                parent = comment.parent()

                if comment.author is not None and parent.author is not None:
                    output.write(comment.author.name + " " + parent.author.name + "\n")
                    output.flush()

            # Once we have a keyboard interupt then we save the graph
            except KeyboardInterrupt as e:
                exit()

