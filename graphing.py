import matplotlib.pyplot as plt

deerPopul = []
wolfPopul = []
time = []

def buildYAxis(fps, frames, interval):
    global time
    sfp = 1 / fps
    data_interval = interval * sfp
    num_data_items = frames // interval

    for i in range(num_data_items):
        time.append(i * data_interval)

def graph(fps, frames, interval):
    buildYAxis(fps, frames, interval)

    # Making subplots
    fig, ax = plt.subplots(2, figsize=(6, 7))
    ax[0].plot(time, deerPopul)
    ax[1].plot(time, wolfPopul)
    fig.tight_layout(h_pad=4.5)

    # Labeling
    ax[0].set_title('Deer Population vs Time')
    ax[1].set_title('Wolf Population vs Time')
    ax[0].set_ylabel('Deer Population')
    ax[1].set_ylabel('Wolf Population')
    ax[0].set_xlabel('Time')
    ax[1].set_xlabel('Time')

    plt.show()
