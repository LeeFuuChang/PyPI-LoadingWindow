from LoadingWindow import LoadingWindow

import time

def fakeTask(loadingwindow: LoadingWindow, percentage):
    try:
        loadingwindow.text = f"Loading... [{percentage} out of 100]" # update loading status text
        loadingwindow.progress = percentage # update loading progress-bar value [0, 100]
        time.sleep(0.1)
        return True # return True if the loading finished successfully
    except Exception as e:
        return False # return False if the loading failed (maybe due to connection-error or other issues...)


window = LoadingWindow()


# Set the Size of the loading Window
window.setSize(500, 300)

# Set the Height of the ProgressBar
window.setFontSize(10)

# Set distance between the Window's Edge and the ProgressBar
window.setPadding(30, 30)

# Set Loading Splash Image
window.setSplashArtPath("./LoadingWindow/default-loading-splash.png")

# Set the tasks to load
window.setTasks([lambda p=i:fakeTask(window, p) for i in range(101)])

# Set Tasks retries
window.setTaskRetries(3)


window.exec_()