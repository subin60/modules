import numpy as np
import random
import pandas as pd
import os
import zipfile
import matplotlib.pyplot as plt
import datetime
import matplotlib.image as mpimg


import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Activation, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import clone_model





import matplotlib.pyplot as plt

def plot_history(history):
  """
  Plots the training and validation loss and accuracy of a trained model.

  Args:
  history: History object. Outputs of the fit() function of a keras model.

  Returns:
  Two plots. One for loss and one for accuracy.
  """
  
  # Importing the necessary library for plotting
  
  
  # Extracting loss and accuracy for both training and validation from the History object
  loss = history.history['loss']
  accuracy = history.history['accuracy']
  val_loss = history.history['val_loss']
  val_accuracy = history.history['val_accuracy']

  # Getting the number of epochs the model was trained for
  epochs = range(len(history.history['loss']))

  # Plotting training and validation loss
  plt.figure()
  plt.plot(epochs, loss, label='training loss')
  plt.plot(epochs, val_loss, label='validation loss')
  plt.title('Loss')  # Title of the plot
  plt.xlabel('Epochs')  # X-axis label
  plt.ylabel('Loss')  # Y-axis label
  plt.legend()  # Legend to differentiate between training and validation loss

  # Plotting training and validation accuracy
  plt.figure()
  plt.plot(epochs, accuracy, label='training accuracy')
  plt.plot(epochs, val_accuracy, label='validation accuracy')
  plt.title('Accuracy')  # Title of the plot
  plt.xlabel('Epochs')  # X-axis label
  plt.ylabel('Accuracy')  # Y-axis label
  plt.legend()  # Legend to differentiate between training and validation accuracy


import os
import zipfile
  
def download_and_unzip(filepath):
  """
  Downloads and unzips a zip file from a specified filepath.

  Args:
  filepath: A string specifying the URL of the zip file to download.

  Returns:
  None.
  """
  # Import necessary libraries
 

  # Use wget to download the zip file
  os.system(f'wget {filepath}')
  
  # Use os.path.basename to get the filename (with extension) from the filepath
  filename_with_extension = os.path.basename(filepath)
  
  # Create a ZipFile object
  zip_ref = zipfile.ZipFile(filename_with_extension, 'r')

  # Extract all the contents of the zip file in current directory
  zip_ref.extractall()

  # Close the ZipFile object
  zip_ref.close()


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import random

def view_random_image(target_dir, target_class):
  """
  Picks and displays a random image from a specified directory and class.

  Parameters:
  target_dir : str
      The target directory where the image classes directories are.
  target_class : str
      The target class from which to pick the image.

  Returns:
  img : numpy.ndarray
      The image array in RGB format.
  """

  # Setup the target directory (we'll view images from here)
  target_folder = os.path.join(target_dir, target_class)

  # Get a random image path from the target directory
  random_image = random.choice(os.listdir(target_folder))

  # Read in the image using matplotlib
  img = mpimg.imread(os.path.join(target_folder, random_image))

  # Plot the image
  plt.imshow(img)
  plt.title(target_class)
  plt.axis("off")

  print(f"Image shape: {img.shape}") # show the shape of the image

  return img


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def pred_and_plot(model, filename, class_names, img_shape=224):
  """
  Function to predict the class of an image and plot it. 
  Args:
  model: TensorFlow model
  filename: string, path to the target image
  class_names: list, contains the class names that the model can predict
  img_shape: int, the size of the image the model was trained on (default is 224)

  Returns:
  None, but prints out the predicted class and an image plot
  """
  

  # Read in the image file
  img = tf.io.read_file(filename)

  # Decode the read file into a tensor and resize it to the img_shape
  img = tf.image.decode_image(img)
  img = tf.image.resize(img, size=[img_shape, img_shape])

  # Rescale the image (divide by 255)
  img = img/255.

  # Expand the dimensions of the image tensor from [img_shape, img_shape, color_channels] 
  # to [1, img_shape, img_shape, color_channels] as the model expects a batch
  img_expanded = tf.expand_dims(img, axis=0) 

  # Make a prediction on the image using the model
  pred = model.predict(img_expanded)

  # Get the predicted class
  if len(pred[0]) > 1: # multi-class
    pred_class = class_names[np.argmax(pred)]
  else: # binary class
    pred_class = class_names[int(tf.round(pred))]

  # Plot the image with predicted class as title
  plt.imshow(img)
  plt.title(f"Prediction: {pred_class}")
  plt.axis(False)
  plt.show()

  
import pathlib
import numpy as np

def get_class_names(train_dir):
  """
  Function to get class names from a directory.

  Args:
  train_dir: str, path to the training directory containing class subdirectories.

  Returns:
  class_names: numpy array, array of class names sorted in alphabetical order.
  """

  # Import necessary libraries

  # Convert input to a pathlib Path object (this allows for handy methods to be used on the input)
  data_dir = pathlib.Path(train_dir)

  # Use the glob method to find all class subdirectories, get their names and sort them
  class_names = np.array(sorted([item.name for item in data_dir.glob('*')]))

  # Return class names
  return class_names



# Import necessary libraries
import tensorflow as tf
import datetime

def create_tensorboard_callback(dir_name, experiment_name):
  """
  Creates a TensorBoard callback instance to store log files.

  This function generates a TensorBoard callback which is designed to be used 
  with a TensorFlow Keras model. The callback will write logs for TensorBoard 
  which allow you to visualize dynamic graphs of your training and test 
  metrics, as well as activation histograms for the different layers in your model.

  Args:
    dir_name (str): Target directory to store TensorBoard log files.
    experiment_name (str): Name of the experiment directory (e.g., 'efficientnet_model_1').

  Returns:
    tensorboard_callback (tf.keras.callbacks.TensorBoard): A TensorBoard callback instance 
    configured with the log directory.
  
  Example:
    tensorboard_cb = create_tensorboard_callback("tensorboard_logs", "exp1")
    model.fit(X_train, y_train, callbacks=[tensorboard_cb])
  """
  
  # Combine directory name, experiment name, and current time to form a log directory
  log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  
  # Create a TensorBoard callback instance
  tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
  
  print(f"Saving TensorBoard log files to: {log_dir}")
  
  # Return the TensorBoard callback instance
  return tensorboard_callback

import os

def walk_through_dir(dir_path):
    """
    Walks through a directory, printing out the number of directories and 
    images (files) in each, along with each subdirectory's name.
    
    Args:
        dir_path (str): The path of the target directory to walk through.
    
    Returns:
        None. However, as a side effect, this function will print:
        - The number of subdirectories in `dir_path`
        - The number of images (or files) in each subdirectory
        - The name of each subdirectory
    """
    # Use os.walk to generate a 3-tuple for each directory it traverses 
    for dirpath, dirnames, filenames in os.walk(dir_path):
        # Get the count of directories and files
        num_dirs = len(dirnames)
        num_files = len(filenames)
        
        # Print the counts and the current directory path
        print(f"There are {num_dirs} directories and {num_files} images in '{dirpath}'.")

