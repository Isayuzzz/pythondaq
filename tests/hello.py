import click
import time
@click.command()
@click.argument("name")
@click.option(
"-c",
"--count",
default=1,

help="Number of times to print greeting.",
show_default=True, # show default in help
)

@click.option(
"-s",
"--seconds",
default=0,

help="Number of seconds to wait before printing again.",
show_default=True, # show default in help
)


@click.option(
"-g",
"--greeting",
default="Hello",

help="Hello or Goodbye.",   
show_default=True, # show default in help
)

def hello(name, count, seconds, greeting):
    for _ in range(count):
        print(f"Hello {name}!")
        # print(f str(greeting))
        time.sleep(seconds) 
if __name__ == "__main__":
    hello()
