import csv
import json
from pathlib import Path
from pprint import pp


def main():
    csv_file = Path("data") / "pyparis2018.csv"
    # csv_reader = csv.reader(csv_file.open(), delimiter=";")
    csv_reader = csv.DictReader(csv_file.open(), delimiter=";")
    talks = []
    for line in csv_reader:
        # pp(line)
        title = tuple(line.values())[0]
        first_name = line["speaker_first_name"]
        last_name = line["speaker_last_name"]
        print(title)
        print(tuple(line.keys()))
        print()
        talks.append(
            {
                "title": title,
                "presenter": f"{first_name} {last_name}",
            }
        )

    (Path("data") / "pyparis2018.json").write_text(json.dumps(talks, indent=2))


main()
