import numpy as np

def make_histogram(df, col="likeScore", bins=20, width=100):
    blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    data = df[col].dropna()
    counts, bin_edges = np.histogram(data, bins=bins)
    max_count = counts.max() if counts.max() > 0 else 1
    for i in range(len(counts)):
        bar_len = int(width * counts[i] / max_count)
        bar = blocks[-1] * bar_len
        print(f'{bin_edges[i]:>8.2f} ~ {bin_edges[i+1]:>8.2f}: {bar} ({counts[i]})')