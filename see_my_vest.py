import click


@click.command()
@click.argument("vesting_events_csv", type=click.File())
@click.argument("target_date", type=click.DateTime(formats=['%Y-%m-%d']))
@click.argument("precision", default=0, type=click.IntRange(0, 6))
def main(vesting_events_csv, target_date, precision):
    click.echo(f"hi {precision}")
    pass


if __name__ == "__main__":
    main()
