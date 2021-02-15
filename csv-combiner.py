import sys
import CSVCombiner


def main():
    csv_combiner = CSVCombiner.CSVCombiner(sys.argv)
    csv_combiner.csv_combine()


if __name__ == "__main__":
    main()
