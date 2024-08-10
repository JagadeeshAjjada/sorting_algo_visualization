'''
Project Name : Sorting Algorithms GUI
Sorting Algorithm : Bubble Sort, Selection Sort, Merge Sort, Insertion Sort, Quick Sort
'''
import random
import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rcParams['toolbar'] = 'None'
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'      # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    '#fff',     # White
]


class MatplotlibWidget(QMainWindow):

    # Declare class var
    xdata = None
    ydata = None
    loop_state = False

    def __init__(self):
        # Constructor
        QMainWindow.__init__(self)

        # Read UI
        loadUi("gui.ui", self)

        self.setWindowIcon(QtGui.QIcon("ico.png"))
        self.setFixedSize(800, 600)
        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)
        self.MplWidget.canvas.axes.get_yaxis().set_visible(False)

        # Connect methods to buttons :
        self.btn_Bubble.clicked.connect(self.bubbleSort)
        self.btn_Insertion.clicked.connect(self.insertSort)
        self.btn_Merge.clicked.connect(self.mergeSort)
        self.btn_Selection.clicked.connect(self.selectSort)
        self.btn_Quick.clicked.connect(self.quickSort)

        # Update Graph when spin-box is changed
        self.spnBars.valueChanged.connect(self.update_new_graph)

        # Call Shuffle method when clicked
        self.btn_Shuffle.clicked.connect(self.Shuffle_bars)

    def new_frame(self, highlight_bar, updated_bar_color=None):

        # Sleep to create a more pleasing animation
        time.sleep(self.ani_time())
        self.MplWidget.canvas.axes.clear()

        # Create colour list to indicate which bar is highlighted
        bar_color = ["#E85853"] * (len(self.ydata)-1)
        bar_color.insert(highlight_bar, "#ffa500")
        if updated_bar_color:
            for ubc in updated_bar_color:
                if ubc != 0:
                    bar_color[ubc-1] = "#6FE853"
                else:
                    bar_color[ubc] = "#6FE853"
        self.draw_graph(self.xdata, self.ydata, bar_color)

        # Process pending envents for the MPL graph
        QtCore.QCoreApplication.processEvents()

    def ani_time(self):
        # Determine sort wait time scaled to bars amount
        ani_speed = self.sldAnim_speed.value()

        # Linear formula that determine the sleep time from the slider value
        ani_interval = (-1/295)*ani_speed + 0.336
        return(ani_interval)

    def Shuffle_bars(self):
        # Shuffle bars in canvas
        self.MplWidget.canvas.axes.clear()

        bar_count = self.spnBars.value()

        scram_ys = [i for i in range(1, bar_count +1)]
        xs = scram_ys.copy()

        for j in range(0, len(scram_ys)-1):
            target = random.randint(j, len(scram_ys)-1)
            scram_ys[j], scram_ys[target] = scram_ys[target], scram_ys[j]

        # Send Shuffled data to class var
        self.ydata = scram_ys.copy()
        self.xdata = xs.copy()

        # Draw new data onto graph
        self.draw_graph(xs, scram_ys, None)
        self.status.setText("Ready For Sorting!")

    def update_new_graph(self):
        # Update canvas on change event from the spin edit
        self.MplWidget.canvas.axes.clear()

        # Create new dataset with changed size
        bar_count = self.spnBars.value()
        ys = [i for i in range(1, bar_count +1)]
        xs = ys.copy()

        # Send data to class var
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        # Draw new data onto graph
        self.draw_graph(xs, ys, None)

    def initial_graph(self):
        # Startup with bars, not empty graph
        self.update_new_graph()

    def draw_graph(self, xs, ys, bar_color):
        # Draw graph from x-list and y-list
        if bar_color is None:
            self.MplWidget.canvas.axes.bar(xs, ys, color="#E85853")
        else:
            # Color parameter will highlight selected bar (Bar that is being moved)
            self.MplWidget.canvas.axes.bar(xs, ys, color=bar_color)

        self.MplWidget.canvas.draw()

    def buttons(self, tfstate):
        self.btn_Bubble.setEnabled(tfstate)
        self.btn_Insertion.setEnabled(tfstate)
        self.btn_Merge.setEnabled(tfstate)
        self.btn_Selection.setEnabled(tfstate)
        self.btn_Quick.setEnabled(tfstate)
        self.btn_Shuffle.setEnabled(tfstate)

    def bubbleSort(self):
        # Copy dataset
        yarray = self.ydata.copy()

        updated_bar_color = []
        # Disable buttons
        self.buttons(False)
        self.status.setText("Bubble Sort Processing!")

        # Disable spin box
        self.spnBars.setDisabled(True)

        # Loop through all elements
        for i in range(len(yarray)):

            # Determine new endpoint as last i elements will be sorted (efficientcy)
            endp = len(yarray) - i
            sorted_j = None
            # Iterate over new resized dataset
            for j in range(0, endp):

                # Prevent loop reaching out of list
                if j+1 == len(yarray):
                    sorted_j = j + 1
                else:
                    if yarray[j] > yarray[j+1]:

                        # Swap elements if not ascending
                        yarray[j], yarray[j+1] = yarray[j+1], yarray[j]

                        # Update class var
                        self.ydata = yarray

                        # Call to update graph
                        self.new_frame(j+1, updated_bar_color)
                        sorted_j = j
                    else:
                        sorted_j = j + 1

            updated_bar_color.append(sorted_j)
            self.new_frame(sorted_j, updated_bar_color)

        self.buttons(True)
        self.spnBars.setDisabled(False)
        self.status.setText("Bubble Sort Done!")

    def insertSort(self):
        # Get class variable
        yarray = self.ydata.copy()
        updated_bar_color = []
        # Disable buttons
        self.buttons(False)
        self.status.setText("Insertion Sort Processing!")

        # Disable spin box
        self.spnBars.setDisabled(True)
        updated_bar_color.append(0)
        count = 1
        for i in range(1, len(yarray)):  # Iterate over the array starting from the second element
            key = yarray[i]  # Store the current element as the key to be inserted in the right position
            j = i-1
            while j >= 0 and key < yarray[j]:  # Move elements greater than key one position ahead
                yarray[j+1] = yarray[j]  # Shift elements to the right
                j -= 1
                self.ydata = yarray
                self.new_frame(j, updated_bar_color)
            yarray[j+1] = key  # Insert the key in the correct position
            count += 1
            updated_bar_color.append(count)
        self.new_frame(count, updated_bar_color)


        self.buttons(True)
        self.spnBars.setDisabled(False)
        self.status.setText("Insertion Sort Done!")

    def mergeSort(self):
        # Copy dataset
        yarray = self.ydata.copy()
        self.status.setText("Merge Sort Processing!")
        # Disable buttons
        self.buttons(False)

        # Disable spin box
        self.spnBars.setDisabled(True)

        yarray = self.mergeSplit(yarray)

        # Update class var
        self.ydata = yarray
        updated_bar_color = yarray
        self.new_frame(0, updated_bar_color)

        self.buttons(True)
        self.spnBars.setDisabled(False)
        self.status.setText("Merge Sort Done!")

    def mergeSplit(self, arr):
        length = len(arr)

        # Return, end of recursion
        if length == 1:
            return(arr)

        midp = length//2

        # Call self to split until return single element, update class var
        arr_1 = self.mergeSplit(arr[:midp])
        self.mergeUpdate(arr_1, self.ydata)
        arr_2 = self.mergeSplit(arr[midp:])
        self.mergeUpdate(arr_2, self.ydata)

        self.new_frame(0)

        # Call merge to sort half lists
        return(self.merge(arr_1, arr_2))

    def mergeUpdate(self, sub_list, main_list):

        # Get index of the sorted elements in the main list
        pos = []
        for value in sub_list:
            pos.append(main_list.index(value))

        # Remove elem from main list
        for v in sub_list:
            main_list.remove(v)

        # Find range
        high = max(pos)
        low = min(pos)

        # Insert same elements back to main list, from sorted list (in order)
        for i in range(low, high+1):
            main_list.insert(i, sub_list[i-low])

    def merge(self, arr_1, arr_2):
        sorted_arr = []

        # Use append and pop, given already sorted lists
        while arr_1 and arr_2:

            if arr_1[0] < arr_2[0]:
                # arr1[0] smaller
                sorted_arr.append(arr_1.pop(0))
            else:
                # arr2[0] smaller
                sorted_arr.append(arr_2.pop(0))

        # Append from sorted sublist, as one of the sub-list will be empty
        while arr_1:
            sorted_arr.append(arr_1.pop(0))

        while arr_2:
            sorted_arr.append(arr_2.pop(0))

        return(sorted_arr)

    def selectSort(self):
        updated_bar_color = []
        last_j = None
        # Get class variable
        yarray = self.ydata.copy()
        self.status.setText("Selection Sort Processing!")
        # Disable buttons
        self.buttons(False)

        # Disable spin box
        self.spnBars.setDisabled(True)

        # Loop through list
        for i in range(len(yarray)):

            #Place holder for smallest number in sublist
            holder = None

            # Iterate over unsorted sublist
            for j in range(i, len(yarray)):

                if (not holder):
                    holder = yarray[j]
                elif yarray[j] < holder:
                    holder = yarray[j]

                sorted_j = j
                # Show iteration
                self.new_frame(j, updated_bar_color)
                last_j = j

            # Read and insert least bar into sorted part
            shifter_index = yarray.index(holder)
            yarray.pop(shifter_index)
            yarray.insert(i, holder)

            # Update class var & graph
            self.ydata = yarray

            updated_bar_color.append(i+1)
            # Update graph
            self.new_frame(shifter_index, updated_bar_color)
            # self.new_frame(shifter_index)
        self.new_frame(last_j, updated_bar_color)

        self.buttons(True)
        self.spnBars.setDisabled(False)
        self.status.setText("Selection Sort Done!")

    def partition(self, arr, start, end):
        pivot = arr[end]
        pIndex = start
        for i in range(start, end):
            if arr[i] <= pivot:
                arr[pIndex], arr[i] = arr[i], arr[pIndex]
                # updated_bar_color.append(pIndex)
                pIndex += 1
                self.new_frame(i)
        arr[pIndex], arr[end] = arr[end], arr[pIndex]
        # updated_bar_color.append(pIndex)
        self.new_frame(pIndex)
        return pIndex

    def quickSortImplementation(self, arr, start, end, ):
        if start < end:
            pIndex = self.partition(arr, start, end)
            self.quickSortImplementation(arr, start, pIndex-1)
            self.quickSortImplementation(arr, pIndex+1, end)

    def quickSort(self):
        arr = self.ydata
        start = 0
        end = len(arr) - 1
        # updated_bar_color = []
        self.status.setText("Quick Sort Processing!")
        # Disable buttons
        self.buttons(False)

        # Disable spin box
        self.spnBars.setDisabled(True)
        self.quickSortImplementation(arr, start, end)

        self.buttons(True)
        self.spnBars.setDisabled(False)
        self.status.setText("Quick Sort Done!")

app = QApplication([])
window = MatplotlibWidget()
window.Shuffle_bars()
window.show()
app.exec_()

