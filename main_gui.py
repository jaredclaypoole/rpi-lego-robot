from typing import Optional

from omegaconf import OmegaConf

import flet as ft
import flet_webview as ftwv

from lego_motors import LegoMotors


class Main:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.on_keyboard_event = self.handle_keypress
        page.add(ft.Text("Lego robot controller"))

        config_path = "./config.yaml"
        config = OmegaConf.load(config_path)
        url = config["video_feed_url"]

        print("Starting BrickPi controller")
        self.lm = LegoMotors()
        self.lm.default_redo_action_on_speed_change = True
        self.lm.max_speed = 100
        self.page.on_disconnect = self.teardown

        self.speed_Text = ft.Text()
        page.add(self.speed_Text)
        self.update_speed_text()

        self.wv = ftwv.WebView(
            url=url,
            on_page_started=lambda _: print("Page started"),
            on_page_ended=lambda _: print("Page ended"),
            on_web_resource_error=lambda e: print("Page error:", e.data),
            expand=True,
        )
        self.wv_stack = ft.Stack(
            [
                ft.Container(expand=1),
                self.wv,
            ],
            expand=1,
        )
        self.wv_container = ft.Container(
            self.wv_stack,
            # ft.Placeholder(),
            width=700,
            height=700,
            # expand=1,
        )
        controls_col = ft.Column(
            [
                ft.Row(
                    [
                        ft.Button("Forward", on_click=self.lm.forward),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    [
                        ft.Button("Left", on_click=self.lm.left),
                        ft.Container(width=30),
                        ft.Button("Stop", on_click=self.lm.stop),
                        ft.Container(width=30),
                        ft.Button("Right", on_click=self.lm.right),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    [
                        ft.Button("Backward", on_click=self.lm.backward),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=100),
                ft.Row(
                    [
                        ft.Button("Decrease Speed", on_click=self.halve_speed),
                        ft.Container(width=45),
                        ft.Button("Increase Speed", on_click=self.double_speed),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )
        self.controls_container = ft.Container(
            controls_col,
            expand=1,
        )
        row = ft.Row(
            [
                self.wv_container,
                self.controls_container,
            ]
        )
        page.add(row)
        # row = ft.Row(
        #     [
        #         ft.Button("Forward", on_click=self.lm.forward),
        #         ft.Button("Stop", on_click=self.lm.stop),
        #         ft.Button("Emergency reset", on_click=self.teardown),
        #     ]
        # )
        # page.add(row)
        print("Done with setup")

    def handle_keypress(self, event: ft.KeyboardEvent) -> None:
        key = event.key.lower()
        if not key or key == "q":
            self.lm.stop()
        elif key == "j":  # decrease speed
            self.halve_speed()
        elif key == "k":  # increase speed
            self.double_speed()
        elif key == "w":
            self.lm.forward()
        elif key == "s":
            self.lm.backward()
        elif key == "a":
            self.lm.left()
        elif key == "d":
            self.lm.right()
        elif key == " " or key == "h":
            self.lm.stop()
        else:
            print(f"Unknown key:  {key}")
    
    def teardown(self, *args) -> None:
        del self.lm
    
    def update_speed_text(self, *args) -> None:
        self.speed_Text.value = f"Speed = {self.lm.speed} / 100"
        self.page.update()
    
    def halve_speed(self, *args) -> None:
        self.lm.halve_speed()
        self.update_speed_text()

    def double_speed(self, *args) -> None:
        self.lm.double_speed()
        self.update_speed_text()


if __name__ == '__main__':
    ft.app(Main)
