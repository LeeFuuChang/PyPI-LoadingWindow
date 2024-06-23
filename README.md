# LoadingWindow

Hit the ⭐ at our [repo](https://github.com/LeeFuuChang/PyPi-LoadingWindow) if this helped!!!

Developed by LeeFuuChang © 2024

## Examples of How To Use

Creating A LoadingWindow

```python
from LoadingWindow import AbstractLoadingWindow

window = AbstractLoadingWindow()
window.exec_()
```

Add Tasks to load

```python
from LoadingWindow import AbstractLoadingWindow

import time

def fakeTask(loadingwindow: AbstractLoadingWindow, percentage):
    try:
        loadingwindow.text = f"Loading... [{percentage} out of 100]" # update loading status text
        loadingwindow.progress = percentage # update loading progress-bar value [0, 100]
        time.sleep(0.1)
        return True # return True if the loading finished successfully
    except Exception as e:
        return False # return False if the loading failed (maybe due to connection-error or other issues...)

window = AbstractLoadingWindow()

# define the tasks to load in a list
tasksToLoad = [lambda p=i:fakeTask(window, p) for i in range(101)]

# Set the tasks to load
window.setTasks(tasksToLoad)
# Update loading status (text, progress) by passing the `window` into the function

window.exec_()
```


## Task Function Structure
```python
def fakeTask(loadingwindow: AbstractLoadingWindow, ...):
    """
    @params:
        loadingwindow: AbstractLoadingWindow
        > pass the window object in so you can update the loading status to your user

    @returns:
        bool
        > True -> task success
        > False -> task failed
    """
    try:
        # ... Do the Setup

        loadingwindow.text = "Describe the loading process to your user"
        loadingwindow.progress = 64 # loading progress (%) [0, 100]

        return True
    except Exception as e:
        # ... Handle the Error
        return False
```


## Useful APIs
Set the Size of the loading Window
```python
AbstractLoadingWindow.setSize(500, 300) # Width and Height
```

Set the Height of the ProgressBar
```python
AbstractLoadingWindow.setBarHeight(30)
```

Set the Loading Status Text's FontSize
```python
AbstractLoadingWindow.setFontSize(10)
```

Set distance between the Window's Edge and the ProgressBar
```python
AbstractLoadingWindow.setPadding(30, 30) # Vertical and Horizontal
```

Set Loading Window FrameRate
```python
AbstractLoadingWindow.setFrameRate(60)
```

Set Loading Window's Icon
> this only works after packing into an executable
```python
AbstractLoadingWindow.setIconPath("./Path/To/Your/Icon")
```

Set Loading Splash Image
```python
AbstractLoadingWindow.setSplashArtPath("./Path/To/Your/Image")
```

Set Tasks to load
```python
AbstractLoadingWindow.setTasks([])
```

Set Tasks retries
```python
AbstractLoadingWindow.setRetries(3)
```

Set How long (in seconds) the loading windows stays after all tasks completed
```python
AbstractLoadingWindow.setPreserveTime(1)
```