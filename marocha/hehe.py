import tensorflow as tf
from GUI import gui_service
import gc
import time

CHA = time.perf_counter()
print(gui_service.get_predicted_data_from_only_price_model(7, 'DAYS', 'BTC'))
tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'HOURS', 'BTC'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'MINUTES', 'BTC'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'DAYS', 'BCH'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'HOURS', 'BCH'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'MINUTES', 'BCH'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'DAYS', 'ETH'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'HOURS', 'ETH'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'MINUTES', 'ETH'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'DAYS', 'LTC'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'HOURS', 'LTC'))
# tf.keras.backend.clear_session()
# print(gui_service.get_predicted_data_from_only_price_model(7, 'MINUTES', 'LTC'))
# tf.keras.backend.clear_session()
MARO = time.perf_counter()

print(MARO - CHA)
