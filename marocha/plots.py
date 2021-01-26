from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime

import requests_module
import data_frames

last_day_in_minutes = data_frames.load_standard_data_frame(requests_module.get_minute_last_day_data())

sns.set_context('paper')
sns.relplot(data=last_day_in_minutes['close'], kind='line')
plt.show()