from track import running_speed, load_track, plot_speed
import logging

# __name__ -> dunder name
if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    logging.basicConfig(
        level='INFO',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
    )

    parser = ArgumentParser(description='Generate box plot of running speed')
    parser.add_argument('csv_file', help='CSV file', type=FileType('r'))
    parser.add_argument('out_file', help='Output file', type=FileType('w'))
    args = parser.parse_args()

    df = load_track(args.csv_file.name)
    speed = running_speed(df)
    ax = plot_speed('2022-01-23', speed)
    ax.figure.savefig(args.out_file.name)


# Example:
# python -m track tests/track.csv /tmp/track.png
