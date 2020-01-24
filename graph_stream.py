import praw
import argparse
import igraph
import yaml

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, required=True,
                        help="path to config yml specifying reddit client info")
    parser.add_argument("--target", type=str, required=True,
                        help="sub reddit you wish to scrape")

    args = parser.parse_args()

    # Open YAML config
    with open(args.config_file, "r") as config_file:
        config = yaml.load(config_file)

    # Get Reddit Client
    reddit = praw.Reddit(client_id=config['id'],
                         client_secret=config['secret'],
                         username=config['user'],
                         password=config['psswd'],
                         user_agent=config['agent'])

    # Get subreddit
    subreddit = reddit.subreddit(args.target_subreddit)
    edges = []
    vertices = []

    # Stream comments until user decides otherwise
    for idx, comment in enumerate(subreddit.stream.comments()):
        try:

            print("Streaming Comments...{}".format(idx), end="\r")
            parent = comment.parent()

            if comment.author is not None and comment.author not in vertices:
                vertices.append(comment.author.name)
            if parent.author is not None and parent.author not in vertices:
                vertices.append(parent.author.name)

            if comment.author is not None and parent.author is not None:
                edges.append((comment.author.name, parent.author.name))

        # Once we have a keyboard interupt then we save the graph
        except KeyboardInterrupt as e:
            print()
            graph = igraph.Graph()
            graph.add_vertices(vertices)
            graph.add_edges(edges)

            print("Steaming Complete: Graph Summary")
            igraph.summary(graph)

            graph.write_graphml("{}.graphml".format(args.target_subreddit))
            exit()
