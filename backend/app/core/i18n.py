translations = {
    "EN": {
        "welcome": "Welcome",
        "selected_lang": "Language selected",
        "order_created": "Order created",
        "order_cancelled": "Order cancelled",
        "delivery_started": "Delivery started",
        "delivery_completed": "Delivery completed",
        "order_accepted": "Order accepted",
        "order_declined": "Order declined",
        "order_transferred": "Order transferred",
        "on_pause": "You are on pause",
        "pause_applied": "Pause applied",
        "order_force_cancelled": "Order force cancelled",
        "order_force_completed": "Order force completed",
        "order_manually_transferred": "Order manually transferred",
        "location_updated": "Location updated",
    },
    "UA": {
        "welcome": "Ласкаво просимо",
        "selected_lang": "Мову обрано",
        "order_created": "Замовлення створено",
        "order_cancelled": "Замовлення скасовано",
        "delivery_started": "Доставку розпочато",
        "delivery_completed": "Доставку завершено",
        "order_accepted": "Замовлення прийнято",
        "order_declined": "Замовлення відхилено",
        "order_transferred": "Замовлення передано",
        "on_pause": "Ви на паузі",
        "pause_applied": "Паузу застосовано",
        "order_force_cancelled": "Замовлення примусово скасовано",
        "order_force_completed": "Замовлення примусово завершено",
        "order_manually_transferred": "Замовлення вручну передано",
        "location_updated": "Локацію оновлено",
    }
}

def translate(key: str, lang: str = "EN"):
    return translations.get(lang, translations["EN"]).get(key, key)