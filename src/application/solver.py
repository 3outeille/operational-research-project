import argparse
import deneigeuse
import drone

def main():
    parser = argparse.ArgumentParser(description="blablablalbablal")
    parser.add_argument("--mode", choices=["drone", "deneigeuse"])
    parser.add_argument("--map", choices=["montreal_graph", "montreal_di_graph", "downtown_montreal_graph", "downtown_montreal_di_graph"])
    parser.add_argument("--iter", choices=['1', '2', '3'])

    args = parser.parse_args()

    if args.mode == "deneigeuse":
        if args.map != "montreal_di_graph" and args.map != "downtown_montreal_di_graph":
            raise ValueError("A directed graph should be used in deneigeuse mode.")
        deneigeuse.run(args.map, args.iter)
    elif args.mode == "drone":
        if args.map != "montreal_graph" and args.map != "downtown_montreal_graph":
            raise ValueError("An undirected graph should be used in drone mode.")
        drone.run(args.map, args.iter)
    else:
        raise ValueError("Invalid mode. Should be either `deneigeuse` or `drone`")

if __name__ == '__main__':
    main()