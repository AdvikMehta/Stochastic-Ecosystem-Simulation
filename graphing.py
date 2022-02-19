import matplotlib.pyplot as plt

def graphPopulation(w, frames):
    print('exec')
    plt.plot(w, frames)
    plt.xlabel('Wolves')
    plt.ylabel('Frames')
    plt.show()