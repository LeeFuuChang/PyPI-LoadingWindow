# LoadingWindow

Hit the ⭐ at our [repo](https://github.com/LeeFuuChang/PyPi-LoadingWindow) if this helped!!!

Developed by LeeFuuChang © 2024

## Examples of How To Use

##### Creating A LoadingWindow
```python
from LoadingWindow import LoadingWindow

window = LoadingWindow()
window.exec_()
```

##### Add Tasks to load
```python
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

# define the tasks to load in a list
tasksToLoad = [lambda p=i:fakeTask(window, p) for i in range(101)]

# Set the tasks to load
window.setTasks(tasksToLoad)
# Update loading status (text, progress) by passing the `window` into the function

window.exec_()
```


## Task Function Structure
```python
def fakeTask(loadingwindow: LoadingWindow, ...):
    """
    @params:
        loadingwindow: LoadingWindow
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

### LoadingWindow

##### Set the Size of the loading Window:
```python
LoadingWindow.setSize(500, 300) # Width and Height
```

##### Set distance between the Window's Edge and the ProgressBar:
```python
LoadingWindow.setPadding(30, 30) # Vertical and Horizontal
```

##### Set the Height of the ProgressBar:
```python
LoadingWindow.setBarHeight(24)
```

##### Set the Loading Status Text's FontSize:
```python
LoadingWindow.setFontSize(10) # this will auto re-render
# or
LoadingWindow.progressBar.setFontSize(10) # this will auto re-render
# or
LoadingWindow.progressBar.fontSize = 10
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set the Loading Status Text's FontColor:
```python
LoadingWindow.setFontColor("#000000") # this will auto re-render
# or
LoadingWindow.progressBar.setFontColor("#000000") # this will auto re-render
# or
LoadingWindow.progressBar.fontColor = "#000000"
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set Loading Window's Icon:
> this only works after packing into an executable
```python
LoadingWindow.setIconPath("./Path/To/Your/Icon") # by path
LoadingWindow.setIconURL("./URL/To/Your/Icon") # by url
```

##### Set Loading Splash Image:
```python
LoadingWindow.setSplashArtPath("./Path/To/Your/Image") # by path
LoadingWindow.setSplashArtURL("./URL/To/Your/Image") # by url
```

##### Set Loading Window FrameRate:
```python
LoadingWindow.setFrameRate(30)
```

##### Set How long (in seconds) the loading windows stays after all tasks completed:
```python
LoadingWindow.setPreserveTime(1)
```

##### Set Tasks to load:
```python
LoadingWindow.setTasks([func1, func2, ...])
```

##### Set Tasks retries:
```python
LoadingWindow.setTaskRetries(3)
```

### ProgressBar
You can access `ProgressBar` instance by `LoadingWindow.progressBar`

##### Set the Loading Status Text
```
ProgressBar.setText("Loading . . .") # this will auto re-render
# or
LoadingWindow.progressBar.text = "Loading . . ."
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set the Loading Progress Value
```
ProgressBar.setProgress(0) # 0 ~ 100 # this will auto re-render
# or
LoadingWindow.progressBar.progress = 0 # 0 ~ 100
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set the Padding of ProgressBar Text
> this changes including status text and progress text
```
ProgressBar.setPadding(0, 16) # Vertical and Horizontal # this will auto re-render
# or
LoadingWindow.progressBar.padding = (0, 16) # Vertical and Horizontal
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set the ProgressBar Text's FontSize:
```python
ProgressBar.setFontSize(10) # this will auto re-render
# or
LoadingWindow.setFontSize(10) # this will auto re-render
# or
LoadingWindow.progressBar.fontSize = 10
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set the ProgressBar Text's FontColor:
```python
ProgressBar.setFontColor("#000000") # this will auto re-render
# or
LoadingWindow.setFontColor("#000000") # this will auto re-render
# or
LoadingWindow.progressBar.fontColor = "#000000"
LoadingWindow.progressBar.updateStyle() # re-render
```

##### Set the ProgressBar filled area's Color
```python
ProgressBar.setFilledColor("#69ca67")
```

##### Set the ProgressBar track's Color
```python
ProgressBar.setBackgroundColor("#ffffff")
```
