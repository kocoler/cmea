from rich.progress import track, Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
import time


def do_step():
    time.sleep(1)


def print_line():
    with Progress(TextColumn("[blue]{task.description}"),
                  BarColumn(bar_width=40),
                  "[progress.percentage]{task.percentage:>3.1f}%",
                  "•",
                  TimeElapsedColumn(),
                  "•",
                  TimeRemainingColumn()) as progress:
        tid = progress.add_task("my task", start=True, total=20.0)
        progress.update(tid, description='ww')
        # progress.update(tid, total=int(200))
        progress.start_task(tid)
        while not progress.finished:
            do_step()
            progress.update(tid, advance=1.0)


with Progress(transient=True) as progress:
    task = progress.add_task("Working", total=2)
    # while not progress.finished:
    do_step()
    progress.update(task, advance=1.0)
    # time.sleep(3)
    # progress.stop_task(task)
    progress.stop()
    time.sleep(3)




