import argparse
import platform

from flask import Flask, render_template

import metrics

app = Flask(__name__)


@app.route('/')
def show_interface():
    return render_template('index.html', **{'system': platform.system(),
                                            'cpu': metrics.CpuMetrics(),
                                            'memory': metrics.MemoryMetrics(),
                                            'network': metrics.NetworkMetrics(),
                                            'storage_io': metrics.StorageIOMetrics()})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    app.debug = parser.parse_args().debug

    app.run()
