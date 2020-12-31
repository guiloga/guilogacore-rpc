import os
import click

from guilogacore_rpc.commands.run import runconsumer
from guilogacore_rpc.commands.init import initconsumer, initproducer

WORKING_DIR = os.getcwd()


@click.group()
def amqp_manager():
    pass


cli_manager = click.CommandCollection(
        help="##### guilogacore-rpc (alias 'gui-rpc') #####\n\n"
             "This is a command line manager to start, run and operate wih consumer/producers.",
        sources=[amqp_manager,])


@amqp_manager.command('runconsumer')
@click.option('-c', '--with-config',
              envvar='CONSUMER_CONFIG_FILEPATH',
              help='the .ini configuration file path to run the consumer. '
                   'Default value gets CONSUMER_CONFIG_FILEPATH environment variable.')
def runconsumer_cmd(with_config, **options):
    """Run an RPC server/consumer.
    """
    runconsumer(with_config, **options)


@amqp_manager.command('initconsumer')
@click.argument('app_name')
@click.option('-E', '--exchange', help='the exchange name.', default='rpc_gateway')
@click.option('-t', '--exchange-type', help='the exchange type.', default='direct')
@click.option('-q', '--queue', help='the queue name.', default='my_queue')
@click.option('-r', '--routing-key', help='the routing key.', default='my_queue')
@click.option('-p', '--prefetch-count', type=int, help='the QOS prefetch count.', default=1)
def initconsumer_cmd(app_name, **options):
    initconsumer(WORKING_DIR, app_name, **options)


@amqp_manager.command('initproducer')
@click.argument('app_name')
@click.option('-E', '--exchange', help='the exchange name.', default='rpc_gateway')
@click.option('-r', '--routing-key', help='the routing key.', default='my_queue')
@click.option('-C', '--consumer', help='the response consumer.', default='')
def init_producer(app_name, **options):
    initproducer(WORKING_DIR, app_name, **options)


@amqp_manager.command('publish')
@click.argument('exchange')
@click.argument('routing_key')
@click.argument('message')
def publish(exchange, routing_key, message):
    pass


@amqp_manager.command('generateconfig')
# @click.option('')
def generate_config():
    pass


if __name__ == '__main__':
    cli_manager()