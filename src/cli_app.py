import argparse

from dialog import Dialog

parser = argparse.ArgumentParser()
parser.add_argument('-q', '--query', type=str, help='Specify the content of the user query')
parser.add_argument('-c', '--conversation_id', type=str, default='conversation_default_id', help='Specify the conversation ID')

args = parser.parse_args()   

dialog = Dialog()
print(dialog.query(args.query, args.conversation_id))