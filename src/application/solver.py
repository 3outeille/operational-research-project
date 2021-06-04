import argparse
import deneigeuse
import drone

def main():
    parser = argparse.ArgumentParser(description="blablablalbablal")
    parser.add_argument("--mode", choices=["drone", "deneigeuse"], default="deneigeuse")
    parser.add_argument("--map", choices=["montreal_graph", "montreal_di_graph", "downtown_montreal_graph", "downtown_montreal_di_graph"], default="downtown_montreal_di_graph")
    parser.add_argument("--algo", choices=['first_match', 'best_match'], help="Only for deneigeuse", default="best_match")
    parser.add_argument("--nb_deneigeuses", type=int, help="Only for deneigeuse", default="1")
    parser.add_argument("--nb_drones", type=int, help="Only for drones", default="1")

    args = parser.parse_args()

    if args.mode == "deneigeuse":
        if args.map != "montreal_di_graph" and args.map != "downtown_montreal_di_graph":
            raise ValueError("A directed graph should be used in deneigeuse mode.")
        deneigeuse.run(args.map, args.algo, args.nb_deneigeuses)
    elif args.mode == "drone":
        if args.map != "montreal_graph" and args.map != "downtown_montreal_graph":
            raise ValueError("An undirected graph should be used in drone mode.")
        drone.run(args.map, args.nb_drones)
    else:
        raise ValueError("Invalid mode. Should be either `deneigeuse` or `drone`")

if __name__ == '__main__':
    main()