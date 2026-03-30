"""
main.py - Inventory Manager Android App (Kivy/KivyMD)
"""

import os
from kivy.utils import platform
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar

import database as db

KV = """
#:import dp kivy.metrics.dp

ScreenManager:
    HomeScreen:
        name: "home"
    ScanScreen:
        name: "scan"
    ListScreen:
        name: "list"
    AnalyticsScreen:
        name: "analytics"
    AdminScreen:
        name: "admin"

<HomeScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "Inventory Manager"
            elevation: 4

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(24)
            spacing: dp(16)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 1, None
            height: self.minimum_height

            Widget:  # top spacer
                size_hint_y: None
                height: dp(40)

            MDRaisedButton:
                text: "SCAN / ADD ITEM"
                size_hint_x: 1
                height: dp(56)
                on_release: app.root.current = "scan"
                md_bg_color: app.theme_cls.primary_color

            MDRaisedButton:
                text: "VIEW / EDIT TRANSACTIONS"
                size_hint_x: 1
                height: dp(56)
                on_release: app.go_to_list()
                md_bg_color: app.theme_cls.primary_color

            MDRaisedButton:
                text: "ANALYTICS"
                size_hint_x: 1
                height: dp(56)
                on_release: app.go_to_analytics()
                md_bg_color: app.theme_cls.primary_color

            MDRaisedButton:
                text: "ADMIN (Import CSV)"
                size_hint_x: 1
                height: dp(56)
                on_release: app.root.current = "admin"
                md_bg_color: [0.4, 0.4, 0.4, 1]

<ScanScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "Scan / Add Item"
            left_action_items: [["arrow-left", lambda x: app.go_home()]]
            elevation: 4

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: barcode_input
                    hint_text: "Scan Barcode"
                    helper_text: "Scan or type barcode then press Enter"
                    helper_text_mode: "on_focus"
                    icon_right: "barcode-scan"
                    on_text_validate: app.lookup_by_barcode(self.text)

                MDTextField:
                    id: itemno_input
                    hint_text: "Item Number (manual)"
                    helper_text: "Type item number then press Enter"
                    helper_text_mode: "on_focus"
                    icon_right: "magnify"
                    on_text_validate: app.lookup_by_itemno(self.text)

                MDCard:
                    padding: dp(12)
                    size_hint_y: None
                    height: dp(120)
                    elevation: 2

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(4)

                        MDLabel:
                            id: desc_label
                            text: "Description: —"
                            theme_text_color: "Secondary"
                            font_style: "Body1"

                        MDLabel:
                            id: picker_label
                            text: "Picker: —"
                            theme_text_color: "Secondary"
                            font_style: "Body1"

                        MDLabel:
                            id: category_label
                            text: "Category: —"
                            theme_text_color: "Secondary"
                            font_style: "Caption"

                MDTextField:
                    id: from_bin_input
                    hint_text: "FROM BIN"
                    icon_right: "arrow-right-bold-box-outline"

                MDTextField:
                    id: to_bin_input
                    hint_text: "TO BIN"
                    icon_right: "arrow-left-bold-box-outline"

                MDTextField:
                    id: qty_input
                    hint_text: "QTY"
                    input_filter: "float"
                    icon_right: "numeric"

                MDRaisedButton:
                    text: "INSERT TRANSACTION"
                    size_hint_x: 1
                    height: dp(52)
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.insert_transaction()

                MDFlatButton:
                    text: "CLEAR FORM"
                    size_hint_x: 1
                    on_release: app.clear_scan_form()

<ListScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "Transactions"
            left_action_items: [["arrow-left", lambda x: app.go_home()]]
            right_action_items: [["refresh", lambda x: app.refresh_list()]]
            elevation: 4

        ScrollView:
            id: list_scroll
            MDBoxLayout:
                id: list_container
                orientation: "vertical"
                padding: dp(8)
                spacing: dp(6)
                size_hint_y: None
                height: self.minimum_height

<AnalyticsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "Analytics"
            left_action_items: [["arrow-left", lambda x: app.go_home()]]
            right_action_items: [["refresh", lambda x: app.refresh_analytics()]]
            elevation: 4

        ScrollView:
            MDBoxLayout:
                id: analytics_container
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height

<AdminScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "Admin - Import CSV"
            left_action_items: [["arrow-left", lambda x: app.go_home()]]
            elevation: 4

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(16)

            MDLabel:
                text: "Import Item Master CSV"
                font_style: "H6"
                size_hint_y: None
                height: dp(40)

            MDTextField:
                id: csv_path_input
                hint_text: "CSV file path"
                helper_text: "Full path to item_master.csv"
                helper_text_mode: "on_focus"
                text: app.default_csv_path()

            MDRaisedButton:
                text: "IMPORT CSV"
                size_hint_x: 1
                height: dp(52)
                on_release: app.import_csv(csv_path_input.text)

            MDLabel:
                id: import_status
                text: ""
                theme_text_color: "Secondary"
                size_hint_y: None
                height: dp(40)

            Widget:
"""


class TransactionCard(MDCard):
    trans_id = NumericProperty(0)


class EditDialogContent(MDBoxLayout):
    pass


class InventoryApp(MDApp):

    current_item = None
    edit_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        db.init_db()
        return Builder.load_string(KV)

    def default_csv_path(self):
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, "data", "item_master_sample.csv")

    # ── Navigation ──────────────────────────────────────────────────────────

    def go_home(self):
        self.root.current = "home"

    def go_to_list(self):
        self.root.current = "list"
        self.refresh_list()

    def go_to_analytics(self):
        self.root.current = "analytics"
        self.refresh_analytics()

    # ── Scan Screen ──────────────────────────────────────────────────────────

    def _populate_item_fields(self, item):
        """Fill in description/picker/category after a successful lookup."""
        self.current_item = item
        screen = self.root.get_screen("scan")
        picker = db.get_picker_for_category(item["category_code"])
        screen.ids.desc_label.text = f"Description: {item['description']}"
        screen.ids.picker_label.text = f"Picker: {picker}"
        screen.ids.category_label.text = f"Category: {item['category_code']}"
        # Sync both input fields
        screen.ids.barcode_input.text = item["barcode"]
        screen.ids.itemno_input.text = item["item_no"]

    def lookup_by_barcode(self, barcode):
        barcode = barcode.strip()
        if not barcode:
            return
        item = db.get_item_by_barcode(barcode)
        if item:
            self._populate_item_fields(item)
        else:
            self._show_snackbar(f"Barcode '{barcode}' not found in item master.")

    def lookup_by_itemno(self, item_no):
        item_no = item_no.strip()
        if not item_no:
            return
        item = db.get_item_by_itemno(item_no)
        if item:
            self._populate_item_fields(item)
        else:
            self._show_snackbar(f"Item '{item_no}' not found in item master.")

    def insert_transaction(self):
        screen = self.root.get_screen("scan")
        if not self.current_item:
            self._show_snackbar("Please scan or enter a valid item first.")
            return

        from_bin = screen.ids.from_bin_input.text.strip()
        to_bin = screen.ids.to_bin_input.text.strip()
        qty_text = screen.ids.qty_input.text.strip()

        if not from_bin or not to_bin or not qty_text:
            self._show_snackbar("Please fill FROM BIN, TO BIN and QTY.")
            return

        try:
            qty = float(qty_text)
        except ValueError:
            self._show_snackbar("QTY must be a number.")
            return

        item = self.current_item
        picker = db.get_picker_for_category(item["category_code"])
        db.insert_transaction(
            item["item_no"],
            item["barcode"],
            item["description"],
            item["category_code"],
            picker,
            from_bin,
            to_bin,
            qty,
        )
        self._show_snackbar("Transaction saved successfully!")
        self.clear_scan_form()

    def clear_scan_form(self):
        self.current_item = None
        screen = self.root.get_screen("scan")
        screen.ids.barcode_input.text = ""
        screen.ids.itemno_input.text = ""
        screen.ids.from_bin_input.text = ""
        screen.ids.to_bin_input.text = ""
        screen.ids.qty_input.text = ""
        screen.ids.desc_label.text = "Description: —"
        screen.ids.picker_label.text = "Picker: —"
        screen.ids.category_label.text = "Category: —"

    # ── List Screen ──────────────────────────────────────────────────────────

    def refresh_list(self):
        screen = self.root.get_screen("list")
        container = screen.ids.list_container
        container.clear_widgets()

        transactions = db.get_all_transactions()
        if not transactions:
            container.add_widget(MDLabel(
                text="No transactions yet.",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="48dp",
            ))
            return

        for t in transactions:
            card = self._build_transaction_card(t)
            container.add_widget(card)

    def _build_transaction_card(self, t):
        card = MDCard(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(4),
            size_hint_y=None,
            height=dp(170),
            elevation=2,
        )

        info_layout = MDBoxLayout(orientation="vertical", spacing=dp(2))

        def lbl(text, style="Body2"):
            label = MDLabel(
                text=text,
                markup=True,
                font_style=style,
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(22),
            )
            return label

        info_layout.add_widget(lbl(f"[b]#{t['id']}[/b]  {t['item_no']} - {t['description'][:30]}", "Body1"))
        info_layout.add_widget(lbl(f"Picker: {t['picker_name']}   Cat: {t['category_code']}"))
        info_layout.add_widget(lbl(f"FROM: {t['from_bin']}  →  TO: {t['to_bin']}   QTY: {t['qty']}"))
        info_layout.add_widget(lbl(f"{t['created_at']}", "Caption"))

        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40),
        )

        trans_id = t["id"]
        edit_btn = MDRaisedButton(
            text="EDIT",
            size_hint_x=0.5,
        )
        edit_btn.bind(on_release=lambda x, tid=trans_id, rec=t: self.open_edit_dialog(tid, rec))

        del_btn = MDRaisedButton(
            text="DELETE",
            size_hint_x=0.5,
            md_bg_color=[0.8, 0.2, 0.2, 1],
        )
        del_btn.bind(on_release=lambda x, tid=trans_id: self.confirm_delete(tid))

        btn_layout.add_widget(edit_btn)
        btn_layout.add_widget(del_btn)

        card.add_widget(info_layout)
        card.add_widget(btn_layout)
        return card

    def open_edit_dialog(self, trans_id, record):
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(200),
        )

        from_field = MDTextField(hint_text="FROM BIN", text=str(record["from_bin"]))
        to_field = MDTextField(hint_text="TO BIN", text=str(record["to_bin"]))
        qty_field = MDTextField(hint_text="QTY", text=str(record["qty"]), input_filter="float")

        content.add_widget(from_field)
        content.add_widget(to_field)
        content.add_widget(qty_field)

        self.edit_dialog = MDDialog(
            title=f"Edit Transaction #{trans_id}",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.edit_dialog.dismiss(),
                ),
                MDRaisedButton(
                    text="SAVE",
                    on_release=lambda x: self._save_edit(trans_id, from_field.text, to_field.text, qty_field.text),
                ),
            ],
        )
        self.edit_dialog.open()

    def _save_edit(self, trans_id, from_bin, to_bin, qty_text):
        try:
            qty = float(qty_text)
        except ValueError:
            self._show_snackbar("QTY must be a number.")
            return
        db.update_transaction(trans_id, from_bin.strip(), to_bin.strip(), qty)
        self.edit_dialog.dismiss()
        self._show_snackbar("Transaction updated.")
        self.refresh_list()

    def confirm_delete(self, trans_id):
        dialog = MDDialog(
            title="Confirm Delete",
            text=f"Delete transaction #{trans_id}?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=[0.8, 0.2, 0.2, 1],
                    on_release=lambda x: self._do_delete(trans_id, dialog),
                ),
            ],
        )
        dialog.open()

    def _do_delete(self, trans_id, dialog):
        db.delete_transaction(trans_id)
        dialog.dismiss()
        self._show_snackbar(f"Transaction #{trans_id} deleted.")
        self.refresh_list()

    # ── Analytics Screen ─────────────────────────────────────────────────────

    def refresh_analytics(self):
        screen = self.root.get_screen("analytics")
        container = screen.ids.analytics_container
        container.clear_widgets()

        stats = db.get_analytics()
        if not stats:
            container.add_widget(MDLabel(
                text="No data yet.",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(48),
            ))
            return

        for s in stats:
            card = MDCard(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(6),
                size_hint_y=None,
                height=dp(130),
                elevation=2,
            )

            def row(text):
                return MDLabel(
                    text=text,
                    font_style="Body2",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=dp(22),
                )

            card.add_widget(MDLabel(
                text=f"[b]{s['picker_name']}[/b]",
                font_style="H6",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(30),
                markup=True,
            ))
            card.add_widget(row(f"Total Items Handled: {s['total_items']}"))
            card.add_widget(row(f"Total QTY: {s['total_qty']}"))
            card.add_widget(row(f"Refilled (FROM ≠ IN0001): {s['refilled']}"))
            card.add_widget(row(f"Newly Added (FROM = IN0001): {s['newly_added']}"))
            container.add_widget(card)

    # ── Admin Screen ─────────────────────────────────────────────────────────

    def import_csv(self, csv_path):
        screen = self.root.get_screen("admin")
        status_lbl = screen.ids.import_status
        csv_path = csv_path.strip()
        if not os.path.exists(csv_path):
            status_lbl.text = f"File not found: {csv_path}"
            status_lbl.theme_text_color = "Error"
            return
        try:
            count = db.import_item_master(csv_path)
            status_lbl.text = f"Imported {count} items successfully."
            status_lbl.theme_text_color = "Custom"
            status_lbl.text_color = [0, 0.6, 0, 1]
        except Exception as e:
            status_lbl.text = f"Error: {e}"
            status_lbl.theme_text_color = "Error"

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _show_snackbar(self, message):
        Snackbar(text=message, snackbar_x="8dp", snackbar_y="8dp",
                 size_hint_x=0.95).open()


if __name__ == "__main__":
    InventoryApp().run()
