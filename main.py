import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Country": ["United Kingdom", "Brazil", "United States", "Afghanistan", "Nigeria"],
    "Median Age": [40, 34, 38, 17, 18]
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
plt.bar(df["Country"], df["Median Age"], color=['blue', 'green', 'red', 'purple', 'orange'])

plt.xlabel("Country")
plt.ylabel("Median Age")
plt.title("Comparison of Median Age by Country")
plt.ylim(0, 50)

plt.show()
