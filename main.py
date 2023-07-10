from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput



class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        start_button = Button(text='Начать')
        start_button.bind(on_release=self.switch_to_second_screen)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def switch_to_second_screen(self, instance):
        self.manager.current = 'second_screen'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Выберите количество игроков:')
        layout.add_widget(label)
        players_layout = BoxLayout()
        two_players_button = Button(text='2 игрока')
        two_players_button.bind(on_release=self.switch_to_third_screen)
        three_players_button = Button(text='3 игрока')
        three_players_button.bind(on_release=self.switch_to_third_screen)
        four_players_button = Button(text='4 игрока')
        four_players_button.bind(on_release=self.switch_to_third_screen)
        players_layout.add_widget(two_players_button)
        players_layout.add_widget(three_players_button)
        players_layout.add_widget(four_players_button)
        layout.add_widget(players_layout)
        self.add_widget(layout)

    def switch_to_third_screen(self, instance):
        num_players = int(instance.text[0])
        self.manager.current = 'third_screen'
        self.manager.get_screen('third_screen').initialize_scoreboard(num_players)


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        self.num_players = 0
        self.scoreboard = []
        self.layout = None

    def initialize_scoreboard(self, num_players):
        self.num_players = num_players
        self.scoreboard = [[0] * 2 for _ in range(num_players)]

        layout = BoxLayout(orientation='vertical')

        table_layout = GridLayout(cols=2, size_hint=(1, 0.8))
        self.cell_labels = []
        for i in range(num_players):
            player_label = Label(text=f'Игрок {i+1}:')
            score_label = Label(text='0')
            self.cell_labels.append(score_label)
            table_layout.add_widget(player_label)
            table_layout.add_widget(score_label)
        layout.add_widget(table_layout)

        player_select_layout = BoxLayout()
        self.player_buttons = []
        for i in range(num_players):
            button = Button(text=f'Игрок {i+1}')
            button.bind(on_release=self.select_player)
            self.player_buttons.append(button)
            player_select_layout.add_widget(button)
        layout.add_widget(player_select_layout)

        self.score_input = TextInput(hint_text='Количество очков')
        layout.add_widget(self.score_input)

        buttons_layout = BoxLayout()
        add_score_button = Button(text='Записать')
        add_score_button.bind(on_release=self.add_score)
        calculate_button = Button(text='Подсчитать все очки')
        calculate_button.bind(on_release=self.calculate_scores)
        buttons_layout.add_widget(add_score_button)
        buttons_layout.add_widget(calculate_button)
        layout.add_widget(buttons_layout)

        if self.layout is not None:
            self.remove_widget(self.layout)  # Удаление предыдущего содержимого ThirdScreen

        self.layout = layout
        self.add_widget(layout)

    def select_player(self, instance):
        for button in self.player_buttons:
            button.background_color = (1, 1, 1, 1)
        instance.background_color = (0, 1, 0, 1)
        self.selected_player = self.player_buttons.index(instance)

    def add_score(self, instance):
        score = int(self.score_input.text)
        self.scoreboard[self.selected_player][0] += score
        self.cell_labels[self.selected_player].text = str(self.scoreboard[self.selected_player][0])
        self.score_input.text = ''

    def calculate_scores(self, instance):
        total_scores = [sum(player_scores) for player_scores in self.scoreboard]
        sorted_scores = sorted(total_scores, reverse=True)
        ranking_text = '\n'.join([f'Место {i+1}: Игрок {total_scores.index(score)+1} ({score} очков)'
                                 for i, score in enumerate(sorted_scores)])

        popup_layout = BoxLayout(orientation='vertical')
        ranking_label = Label(text=ranking_text)
        play_again_button = Button(text='Еще раз')
        play_again_button.bind(on_release=self.reset_scoreboard)
        go_home_button = Button(text='Домой')
        go_home_button.bind(on_release=self.go_to_start_screen)
        popup_layout.add_widget(ranking_label)
        popup_layout.add_widget(play_again_button)
        popup_layout.add_widget(go_home_button)

        popup = Popup(title='Рейтинг игроков', content=popup_layout,
                      size_hint=(None, None), size=(400, 400))
        popup.open()
        self.popup = popup

    def reset_scoreboard(self, instance):
        self.scoreboard = [[0] * 2 for _ in range(self.num_players)]
        for label in self.cell_labels:
            label.text = '0'
        self.popup.dismiss()  # Закрытие всплывающего окна
        self.remove_widget(self.layout)  # Удаление содержимого ThirdScreen
        self.layout = None

    def go_to_start_screen(self, instance):
        self.reset_scoreboard(instance)
        self.manager.current = 'start_screen'
        self.popup.dismiss()  # Закрытие всплывающего окна


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start_screen'))
        sm.add_widget(SecondScreen(name='second_screen'))
        sm.add_widget(ThirdScreen(name='third_screen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
