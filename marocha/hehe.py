import tensorflow as tf
from GUI import gui_service

print(gui_service.get_predicted_data_from_only_price_model(7,'DAYS'))
print(gui_service.get_predicted_data_from_only_price_model(7,'HOURS'))
print(gui_service.get_predicted_data_from_only_price_model(14,'MINUTES'))