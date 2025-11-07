import sys
import subprocess
import threading
import itertools
import time
import argparse
import os
from ollama import chat

def get_response(model: str, messages: list[dict[str, str]]):
    '''Stream the model's response token by token.'''
    response = chat(model=model, messages=messages)
    return response['message']['content']


def loader(stop_event):
    '''Display a simple loading spinner until stop_event is set.'''
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r Generating...{c}')
        sys.stdout.flush()
        time.sleep(0.1)


def main():
    parser = argparse.ArgumentParser(
        description='Ask a local LLM (via Ollama) a question and pretty-print the result.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "<prompt>"
  %(prog)s "<prompt>" --model mistral:latest
  %(prog)s "<prompt>" --keep
'''
    )

    parser.add_argument('prompt', help='The prompt or question to send to the model.')
    parser.add_argument(
        '-m', '--model',
        default='llama3:latest',
        help='Model to use (default: llama3:latest)'
    )
    parser.add_argument(
        '--keep',
        action='store_true',
        help='Keep the generated "res.md" file instead of deleting it after display.'
    )

    args = parser.parse_args()

    stop_event = threading.Event()
    spinner = threading.Thread(target=loader, args=(stop_event,))
    spinner.start()

    try:
        response_text = get_response(args.model, [{'role': 'user', 'content': args.prompt}])
    except Exception as e:
        stop_event.set()
        spinner.join()
        print(f"\nError: {e}")
        sys.exit(1)

    stop_event.set()
    spinner.join()

    output_path = 'res.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(response_text)

    sys.stdout.write("\n")

    # Display with batcat (fallback to cat if batcat is missing)
    try:
        subprocess.run(['batcat', '-l', 'markdown', '--paging=never', output_path], check=True)
    except FileNotFoundError:
        subprocess.run(['cat', output_path])

    # Delete or keep file based on the flag
    if not args.keep:
        os.remove(output_path)
    else:
        print(f'\nOutput saved as {output_path}')


if __name__ == '__main__':
    main()
