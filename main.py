import re
import shlex
from typing import get_type_hints

from docopt import docopt
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from AgentMenu import AgentMenu
from EmpireCliState import state
from ListenerMenu import ListenerMenu
from MainMenu import MainMenu
from UseListenerMenu import UseListenerMenu
from UseStagerMenu import UseStagerMenu


class MyCustomCompleter(Completer):
    def __init__(self, empire_cli):
        self.empire_cli = empire_cli

    def get_completions(self, document, complete_event):
        cmd_line = list(map(lambda s: s.lower(), shlex.split(document.current_line)))
        if len(cmd_line) > 0:
            if cmd_line[0] in ['uselistener']:
                return self.empire_cli.menus['UseListenerMenu'].get_completions(document, complete_event)
            if cmd_line[0] in ['usestager']:
                return self.empire_cli.menus['UseStagerMenu'].get_completions(document, complete_event)

        return self.empire_cli.current_menu.get_completions(document, complete_event)


class EmpireCli(object):

    def __init__(self) -> None:
        self.completer = MyCustomCompleter(self)
        self.menus = {
            'MainMenu': MainMenu(),
            'ListenerMenu': ListenerMenu(),
            'UseListenerMenu': UseListenerMenu(),
            'UseStagerMenu': UseStagerMenu(),
            'AgentMenu': AgentMenu(),
        }
        self.current_menu = self.menus['MainMenu']

    def autocomplete(self):
        return self.current_menu.autocomplete()

    def bottom_toolbar(self):
        # TODO This will read number of listeners, agents, etc from the state
        return HTML('Connected to <b><style bg="ansired">https://localhost:1337</style></b>. 6 agents.')

    @staticmethod
    def strip(options):
        return {re.sub('[^A-Za-z0-9 _]+', '', k): v for k, v in options.items()}

    def main(self):
        # Create some history first. (Easy for testing.)
        history = InMemoryHistory()
        history.append_string("help")
        history.append_string('uselistener http')
        history.append_string('listeners')
        history.append_string("main")

        print('Welcome to Empire!')
        print("Use the 'connect' command to connect to your Empire server.")
        print("connect localhost will connect to a local empire instance with all the defaults")
        print("including the default username and password.")

        session = PromptSession(
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
            completer=self.completer,
            bottom_toolbar=self.bottom_toolbar
        )

        while True:
            try:
                with patch_stdout():
                    text = session.prompt(HTML((f"<ansiblue>{self.current_menu.display_name}</ansiblue> > ")))
                # cmd_line = list(map(lambda s: s.lower(), shlex.split(text)))
                # TODO what to do about case sensitivty for parsing options.
                    cmd_line = list(shlex.split(text))
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

            if len(cmd_line) == 0:
                continue
            if not state.connected and not cmd_line[0] == 'connect':
                continue
            # Switch Menus
            if text == 'main':
                self.current_menu = self.menus['MainMenu']
            elif text == 'listeners':
                self.current_menu = self.menus['ListenerMenu']
            elif cmd_line[0] == 'uselistener' and len(cmd_line) > 1:
                if len(list(filter(lambda x: x == cmd_line[1], self.menus['UseListenerMenu'].listener_types['types']))) > 0:
                    # todo utulize the command decorator?
                    self.current_menu = self.menus['UseListenerMenu']
                    self.current_menu.use(cmd_line[1])
                else:
                    print(f'No module {cmd_line[1]}')
            elif cmd_line[0] == 'usestager' and len(cmd_line) > 1:
                if len(list(filter(lambda x: x == cmd_line[1], list(map(lambda x: x['Name'], self.menus['UseStagerMenu'].stagers['stagers']))))) > 0:
                    # todo utulize the command decorator?
                    self.current_menu = self.menus['UseStagerMenu']
                    self.current_menu.use(cmd_line[1])
                else:
                    print(f'No module {cmd_line[1]}')
            elif text == 'stagers':
                self.current_menu = self.menus['StagerMenu']
            elif text == 'agents':
                self.current_menu = self.menus['AgentMenu']
            else:
                func = None
                try:
                    func = getattr(self.current_menu if hasattr(self.current_menu, cmd_line[0]) else self, cmd_line[0])
                except:
                    pass

                if func:
                    try:
                        args = self.strip(docopt(
                            func.__doc__,
                            argv=cmd_line[1:]
                        ))
                        # ST does this in the @command decorator
                        new_args = {}
                        # todo casting for typehinted values
                        for key, hint in get_type_hints(func).items():
                            # if args.get(key) is not None:
                            if key is not 'return':
                                new_args[key] = args[key]
                        print(new_args)
                        func(**new_args)
                    except Exception as e:
                        print(e)
                        pass


if __name__ == "__main__":
    empire = EmpireCli()
    empire.main()
