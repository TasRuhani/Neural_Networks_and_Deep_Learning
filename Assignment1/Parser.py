# parser.py

import re

LOG_FILE = "ExperimentLogs.txt"
OUTPUT_FILE = "graph_data.py"


def parse_log_file():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split experiments
    experiments = content.split("============================================================")

    data = {}

    for exp in experiments:
        if "Activation Function:" not in exp:
            continue

        # Extract metadata
        activation = re.search(r"Activation Function:\s*(.+)", exp)
        hidden_layers = re.search(r"Hidden Layers:\s*(\d+)", exp)

        if not activation or not hidden_layers:
            continue

        activation = activation.group(1).strip()
        hidden_layers = hidden_layers.group(1).strip()

        key = f"{activation.replace(' ', '_')}_{hidden_layers}"

        train_losses = []
        val_losses = []
        train_accs = []
        val_accs = []

        epoch_pattern = re.compile(
            r"Epoch\s+\d+:\s+Train Loss=([\d\.]+),\s+Train Acc=([\d\.]+)%,\s+Val Loss=([\d\.]+),\s+Val Acc=([\d\.]+)%"
        )

        for match in epoch_pattern.finditer(exp):
            train_losses.append(float(match.group(1)))
            train_accs.append(float(match.group(2)))
            val_losses.append(float(match.group(3)))
            val_accs.append(float(match.group(4)))

        data[key] = {
            "train_loss": train_losses,
            "val_loss": val_losses,
            "train_acc": train_accs,
            "val_acc": val_accs,
        }

    return data


def write_graph_data(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("graph_data = ")
        f.write(repr(data))


if __name__ == "__main__":
    parsed_data = parse_log_file()
    write_graph_data(parsed_data)
    print("graph_data.py generated successfully.")
