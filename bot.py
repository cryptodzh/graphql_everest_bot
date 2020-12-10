from python_graphql_client import GraphqlClient
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram.utils.request import Request
import logging
import os, sys

BOT_TOKEN = '1485064394:AAHfViNFymBLXXWS84g6hj4XtF0r1wuGApY'


client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/graphprotocol/everest")

def findProject(name):
  query = """
   query findProject($name: String!) {
    projectSearch (text: $name) {
      id
      name
      avatar
      description
      website
      twitter
      github
      isRepresentative
    }
  }
  """
  data = client.execute(query=query, variables={"name":name})
  return data['data']['projectSearch']


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def search(update: Update, context: CallbackContext) -> None:

    if len(context.args) == 0:
        err_msg = 'You should specify project name,\n'
        err_msg += '/search <everest_project_name> \n (e.g. /search Bankroll)'
        update.message.reply_text(err_msg)
        return


    project_name = context.args[0]
    project_info = findProject(context.args[0])

    if len(project_info) == 0:
        update.message.reply_text( f'Couldn\'t find project by name {project_name}!')
        return
    else:
        res_info = "\n".join(("{}={}".format(*i) for i in project_info[0].items()))


    update.message.reply_text(res_info)


def start(update: Update, context: CallbackContext) -> None:

    msg = 'Bot uses api from the subgraph https://thegraph.com/explorer/subgraph/graphprotocol/everest\n\n'
    msg += 'To get data use command /search <everest_project_name> \n (e.g. /search Bankroll)\n'
    update.message.reply_text(msg)


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('/search <everest_project_name> - to get everest project description')

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    updater = Updater(BOT_TOKEN, use_context=True)

    dsp = updater.dispatcher
    dsp.add_handler(CommandHandler("search", search, pass_args=True))
    dsp.add_handler(CommandHandler("start", start))
    dsp.add_handler(CommandHandler("help", help))

    # log all errors
    dsp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()
    print('running')


    updater.idle()

if __name__ == '__main__':
    main()