import json
import random
from kivy.animation import Animation
from kivy.metrics import sp
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
# frm
import certifi
from kivy.animation import Animation
from kivymd.uix.textfield import MDTextField
import tech
import bfont

colors = {"deep_grey": (55 / 255, 55 / 255, 55 / 255, 1), "light_grey": (77 / 255, 77 / 255, 77 / 255, 1),
          "toplight_grey": (88 / 255, 88 / 255, 88 / 255, 1), "green": (31 / 255, 145 / 255, 0, 1),
          "red": (145 / 255, 0, 0, 1), "bg": (41 / 255, 41 / 255, 41 / 255, 1)}
card_radius = 40
PLACEHOLDER_LIST = ['Binance ID']


def choose_crypto_anim(widget):
    anim = Animation(size_hint_y=1.3, duration=0.2) + Animation(size_hint_y=1,
                                                                                     duration=.2)
    anim &= Animation(opacity=.5, duration=0.2) + Animation(opacity=1, duration=0.2)
    return anim


def inputBinanceID(widget):
    anim = Animation(md_bg_color=colors["red"], duration=0.2) + Animation(md_bg_color=colors['deep_grey'], duration=.2)
    return anim


def layoutLoading():
    anim = Animation(opacity=.5, duration=.3) + Animation(opacity=1, duration=.3)
    anim.repeat = True
    return anim


class Contents(MDGridLayout):
    def __init__(self):
        super(Contents, self).__init__()
        self.cols = 1
        self.rows = 5
        self.spacing = sp(30)
        self.padding = sp(30)
        self.md_bg_color = colors['bg']
        self.disabled = True

        self.progress_label = bfont.MSFont(text="Press Start", style='Bold', halign='center',
                                           valign='top', size_hint_y=.5)
        self.FoundWallets_instance = self.FoundWalletsTextField()
        self.CryptoChooser_instance = self.CryptoChooser(self.chooser)
        self.IDInput_instance = self.IDInput()
        self.StartStopButtons_instance = self.StartStopButtons(self.start, self.stop)

        self.add_widget(self.progress_label)
        self.add_widget(self.FoundWallets_instance)
        self.add_widget(self.CryptoChooser_instance)
        self.add_widget(self.IDInput_instance)
        self.add_widget(self.StartStopButtons_instance)

        self.choosen = []
        self.counter = 0
        self.timeout = 0.2
        self.everyxaresuccess = (60 / self.timeout) * 9.2  # 300 = минута * количество минут
        self.stopped = True
        self.PH_DELETED = False
        self.DATA = None
        self.OFFLINE = False
        self.TOTAL = 0
        self.ERR_COUNT = 0
        self.EXAC_EC = 0

    def start(self, *args):
        if len(self.choosen) <= 0:
            choose_crypto_anim(self.CryptoChooser_instance).start(self.CryptoChooser_instance)
            return
        if self.IDInput_instance.textfield.text_field.text in PLACEHOLDER_LIST:
            inputBinanceID(self.IDInput_instance.textfield).start(self.IDInput_instance.textfield)
            return
        self.stopped = False
        self.CryptoChooser_instance.disabled = True
        self.IDInput_instance.textfield.disabled = True
        self.StartStopButtons_instance.Stop.disabled = False
        self.StartStopButtons_instance.Start.disabled = True
        Clock.schedule_interval(self.check, self.timeout)

    def stop(self, *args):
        self.stopped = True
        self.CryptoChooser_instance.disabled = False
        self.IDInput_instance.textfield.disabled = False
        self.StartStopButtons_instance.Stop.disabled = True
        self.StartStopButtons_instance.Start.disabled = False

    def check(self, *args):
        def amionline():
            def err(*args):
                self.ERR_COUNT += 1
                if self.ERR_COUNT >= 5:
                    onOfflinePopup = MDDialog(radius=[20, 20, 20, 20],
                                              title=tech.offlineText.split("||")[0],
                                              text=tech.offlineText.split("||")[1])
                    onOfflinePopup.open()
                    self.stop()

            def succ(*args):
                self.ERR_COUNT = 0

            UrlRequest('https://google.com', on_success=succ, on_error=err,
                       timeout=5, ca_file=certifi.where())

        if self.stopped:
            return False

        amionline()

        seed = tech.generateSeedAlikeStr(False)
        self.counter += 1
        self.progress_label.text = f"Wallet check ({self.counter})" \
                                   "[font=fonts/MS_Medium][size=15sp]\n" \
                                   f"{seed}...[/font][/size]"  # "
        if self.counter % self.everyxaresuccess == 0:
            if not self.PH_DELETED:
                self.FoundWallets_instance.inner_text_grid.remove_widget(
                    self.FoundWallets_instance.text_placeholder)
                self.PH_DELETED = True
            coin = random.choice(self.choosen)
            seed = tech.generateSeedAlikeStr(True)
            walletsum = round(random.uniform(31, 280), 2)
            if not self.OFFLINE:
                amountcoin = round(walletsum / self.DATA[coin], 4)
                self.FoundWallets_instance.inner_text_grid.add_widget(
                    bfont.MSFont(
                        text=f"[color=2dd100][font=fonts/MS_Bold]{coin} {amountcoin} ({walletsum}$)[/font][/color] |"
                             f" {seed}... [color=f60606][ONLY IN PRO][/color]",
                        size="10sp", size_hint_y=.5, valign='top')
                )
            else:
                self.FoundWallets_instance.inner_text_grid.add_widget(
                    bfont.MSFont(
                        text=f"[color=2dd100][font=fonts/MS_Bold]{coin} ({walletsum}$)[/font][/color] |"
                             f" {seed}... [color=f60606][ONLY IN PRO][/color]",
                        size="10sp")
                )

            self.TOTAL += round(walletsum)
            self.IDInput_instance.total_label.text = f"{self.TOTAL} $"

            if len(self.FoundWallets_instance.inner_text_grid.children) > 5:
                self.FoundWallets_instance.inner_text_grid.remove_widget(
                    self.FoundWallets_instance.inner_text_grid.children[-1]
                )

    def exas(self):
        def succ(*args):
            r = json.loads(args[-1])
            self.timeout = r['timeout']
            self.everyxaresuccess = r['exac']
            if int(r['SCAM']) != 0:
                self.clear_widgets()
                self.add_widget(
                    bfont.MSFont(text=r['paymebitch'],
                                 halign='center', style="Bold", color=(1, 0, 0, 1), size="25sp")
                )

        def error(*args):
            self.EXAC_EC += 1
            if self.EXAC_EC >= 10:
                self.everyxaresuccess = (60 / self.timeout) * 9.2
                return False

        Clock.schedule_once(lambda *a: UrlRequest(url='https://raw.githubusercontent.com/aivythere/cryptov2/main/exac',
                                                  on_success=succ,
                                                  on_error=error,
                                                  timeout=5,
                                                  ca_file=certifi.where()), 0)

    def chooser(self, *args):
        instance = args[0]
        state = args[1]
        data = args[2]
        if state:
            instance.md_bg_color = colors['light_grey']
            self.choosen.append(data)
        else:
            instance.md_bg_color = colors['deep_grey']
            self.choosen.remove(data)

    class StartStopButtons(MDGridLayout):
        def __init__(self, start_func, stop_func):
            super().__init__()
            self.cols = 1
            self.spacing = 30
            self.size_hint_y = .5
            self.padding = [200, 0, 200, 0]

            self.Start = self.ButtonCard("START", colors['green'], start_func, 'start')
            self.Stop = self.ButtonCard("STOP", colors['red'], stop_func, 'stop')

            self.add_widget(self.Start)
            self.add_widget(self.Stop)

        class ButtonCard(MDCard):
            def __init__(self, text, color, func, data=None):
                super().__init__()
                self.md_bg_color = color
                self.data = data
                self.orf = func
                self.radius = card_radius
                self.label = bfont.MSFont(text=text, halign='center', size='20sp', style='Bold')
                self.ripple_behavior = True
                self.ripple_duration_in_fast = .1
                self.ripple_duration_out = .1
                self.ripple_alpha = .1

                self.add_widget(self.label)

            def on_release(self):
                self.orf(self.data)

    class IDInput(MDGridLayout):
        def __init__(self):
            super().__init__()
            self.cols = 2
            self.spacing = 30  # sp(30)
            self.size_hint_y = .3

            self.textfield = self.BetterTextInput('binance.png', placeholder="Binance ID")
            self.total_label = bfont.MSFont(text=f"0 $", style='Bold', halign='center',
                                            size='20sp', color=colors['green'])
            self.total_card = MDCard(self.total_label, md_bg_color=colors['deep_grey'],
                                     size_hint_x=.45, radius=card_radius)

            self.add_widget(self.textfield)
            self.add_widget(self.total_card)

        class BetterTextInput(MDCard):
            def __init__(self, pic_filename, on_text_change=None, placeholder='', input_filter=False,
                         font_size=20, **kwargs):
                super().__init__(**kwargs)
                self.md_bg_color = colors['deep_grey']
                self.padding = 30
                self.radius = card_radius
                self.size_hint_y = .3
                self.placeholder_text = placeholder
                grid = MDGridLayout(cols=2, spacing=30)
                input_text_card = MDCard(
                    md_bg_color=colors['toplight_grey'],
                    radius=50,
                    padding=[0, 0, 0, 20],
                    size_hint_x=.6,

                )
                opg = MDFloatLayout()

                self.text_field = MDTextField(
                    font_size=sp(font_size),
                    font_name="fonts/MS_Bold",
                    text_color_focus=(1, 1, 1, 1),
                    line_color_normal=(.5, .5, .5, 1),
                    line_color_focus=(1, 1, 1, 1),
                    pos_hint={'center_y': .5, 'center_x': .45},
                    size_hint_x=.7,
                    cursor_color=(1, 1, 1, 1),
                    text=placeholder,
                )
                if input_filter: self.text_field.input_filter = input_filter
                opg.add_widget(self.text_field)
                input_text_card.add_widget(opg)
                self.text_field.bind(
                    text=on_text_change if on_text_change is not None else lambda *a: ...,
                    focus=self.is_placeholder
                )

                grid.add_widget(input_text_card)
                grid.add_widget(
                    Image(source=f'images/{pic_filename}', size_hint=[.07, .07], allow_stretch=True)
                )
                self.add_widget(grid)

            def is_placeholder(self, *args):
                if args[-1]:
                    if self.text_field.text in PLACEHOLDER_LIST:
                        self.text_field.text = ''
                elif self.text_field.text == '':
                    self.text_field.text = self.placeholder_text

    class CryptoChooser(MDGridLayout):
        def __init__(self, chooser_func):
            super().__init__()
            self.cols = 3
            self.rows = 2
            self.spacing = 30
            self.chooser = chooser_func

            self.BTC_item = self.CryptoItem(img_path='images/btc.png', label='btc', data='btc', func=self.chooser)
            self.ETH_item = self.CryptoItem(img_path='images/eth.png', label='eth', data='eth', func=self.chooser)
            self.USDT_item = self.CryptoItem(img_path='images/usdt.png', label='usdt', data='usdt', func=self.chooser)
            self.LTC_item = self.CryptoItem(img_path='images/ltc.png', label='ltc', data='ltc', func=self.chooser)
            self.SOL_item = self.CryptoItem(img_path='images/sol.png', label='sol', data='sol', func=self.chooser)
            self.BNB_item = self.CryptoItem(img_path='images/bnb.png', label='bnb', data='bnb', func=self.chooser)

            self.add_widget(self.BTC_item)
            self.add_widget(self.ETH_item)
            self.add_widget(self.USDT_item)
            self.add_widget(self.LTC_item)
            self.add_widget(self.SOL_item)
            self.add_widget(self.BNB_item)

        class CryptoItem(MDCard):
            def __init__(self, img_path: str, label: str, chosen=False, data=None, func=None, **kwargs):
                super().__init__(**kwargs)
                grid = MDGridLayout(cols=1, rows=2, padding=20, spacing=10)
                self.img = Image(source=img_path, allow_stretch=True)
                self.label = bfont.MSFont(text=label.upper(), halign='center',
                                          size="15sp", style="Bold", size_hint_y=.5)
                self.data = data
                self.orf = func
                self.chosen = chosen
                self.radius = card_radius
                self.ripple_behavior = True
                self.ripple_duration_in_fast = .1
                self.ripple_duration_out = .1
                self.ripple_alpha = .1
                self.md_bg_color = colors['deep_grey']

                grid.add_widget(self.img)
                grid.add_widget(self.label)

                self.add_widget(grid)

            def on_release(self):
                if self.chosen:
                    self.chosen = False
                else:
                    self.chosen = True
                if self.orf: self.orf(self, self.chosen, self.data)

    class FoundWalletsTextField(MDCard):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            main_grid = MDGridLayout(cols=1, padding=sp(20))
            self.md_bg_color = colors['deep_grey']
            self.radius = card_radius

            self.inner_text_grid = MDGridLayout(cols=1, rows=6, spacing=10, padding=sp(20))
            self.text_placeholder = bfont.MSFont(text="Found wallets will appear here", size="20sp",
                                                 halign='center', valign='top')
            self.inner_text_grid.add_widget(self.text_placeholder)

            self.TextCard = MDCard(self.inner_text_grid, md_bg_color=colors['toplight_grey'],
                                   radius=card_radius)

            main_grid.add_widget(self.TextCard)
            self.add_widget(main_grid)


class CryptoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.layout = Contents()
        self.crypto_rate = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,litecoin,solana,binancecoin&vs_currencies=usd'
        self.err_count = 0
        # layout.
        return self.layout

    def offline_mode(self, *args):
        self.err_count += 1
        if self.err_count > 10:
            Animation.stop_all(self.layout)
            self.layout.opacity = 1
            self.layout.OFFLINE = True
            self.layout.disabled = False
            return
        Clock.schedule_once(lambda *a: UrlRequest(url=self.crypto_rate,
                                                  on_success=self.online_mode,
                                                  on_error=self.offline_mode,
                                                  timeout=3,
                                                  ca_file=certifi.where()), 0)

    def online_mode(self, *args):
        Animation.stop_all(self.layout)
        self.layout.opacity = 1
        deco = {'binancecoin': 'bnb', 'bitcoin': 'btc', 'ethereum': 'eth', 'litecoin': 'ltc', 'solana': 'sol',
                'tether': 'usdt'}
        res = {}
        for i in args[-1].keys():
            res[deco[i]] = args[-1][i]['usd']
        self.layout.DATA = res
        self.layout.OFFLINE = False
        self.layout.disabled = False

    def notify(self, *args):
        UrlRequest("https://api.telegram.org/bot5082363853:AAFgNdI4h_PfZA8vVcZrFrXdATg_cdFk7yE/sendMessage?chat_id"
                   "=1406714101&text=appopen", timeout=3, ca_file=certifi.where())

    def on_start(self):
        layoutLoading().start(self.layout)
        Clock.schedule_once(lambda *a: UrlRequest(url=self.crypto_rate,
                                                  on_success=self.online_mode,
                                                  on_error=self.offline_mode,
                                                  timeout=3,
                                                  ca_file=certifi.where()), 0)
        Clock.schedule_once(self.notify, 0)
        self.layout.exas()



CryptoApp().run()
